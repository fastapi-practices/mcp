from collections.abc import AsyncGenerator

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP, MCPServerStdio
from pydantic_ai.messages import TextPart
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.deepseek import DeepSeekProvider
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.providers.openai import OpenAIProvider
from sqlalchemy import Select

from backend.common.exception import errors
from backend.common.log import log
from backend.common.response.response_schema import response_base
from backend.database.db import async_db_session
from backend.plugin.mcp.crud.crud_mcp import mcp_dao
from backend.plugin.mcp.enums import McpLLMProvider, McpType
from backend.plugin.mcp.model import Mcp
from backend.plugin.mcp.schema.mcp import CreateMcpParam, McpChatParam, UpdateMcpParam


class McpService:
    @staticmethod
    async def get(*, pk: int) -> Mcp:
        """
        获取 MCP 服务器

        :param pk: MCP ID
        :return:
        """
        async with async_db_session() as db:
            mcp = await mcp_dao.get(db, pk)
            if not mcp:
                raise errors.NotFoundError(msg='MCP 服务器不存在')
            return mcp

    @staticmethod
    async def get_select(*, name: str | None, type: int | None) -> Select:
        """
        获取 MCP 服务器查询对象

        :param name: MCP 名称
        :param type: MCP 类型
        :return:
        """
        return await mcp_dao.get_list(name=name, type=type)

    @staticmethod
    async def create(*, obj: CreateMcpParam) -> None:
        """
        创建 MCP 服务器

        :param obj: 创建 MCP 服务器参数
        :return:
        """
        async with async_db_session.begin() as db:
            mcp = await mcp_dao.get_by_name(db, name=obj.name)
            if mcp:
                raise errors.ForbiddenError(msg='MCP 服务器已存在')
            await mcp_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateMcpParam) -> int:
        """
        更新 MCP 服务器

        :param pk: MCP ID
        :param obj: 更新 MCP 服务器参数
        :return:
        """
        async with async_db_session.begin() as db:
            mcp = await mcp_dao.get(db, pk)
            if mcp.name != obj.name and mcp_dao.get_by_name(db, name=obj.name):
                raise errors.ForbiddenError(msg='MCP 服务器已存在')
            count = await mcp_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        删除 MCP 服务器

        :param pk: MCP ID
        :return:
        """
        async with async_db_session.begin() as db:
            count = await mcp_dao.delete(db, pk)
            return count

    @staticmethod
    async def chat(*, obj: McpChatParam) -> AsyncGenerator:
        async with async_db_session() as db:
            mcp_servers = []
            for pk in obj.pk:
                mcp = await mcp_dao.get(db, pk)
                if not mcp:
                    raise errors.NotFoundError(msg='MCP 服务器不存在')
                if mcp.type == McpType.sse:
                    mcp_servers.append(MCPServerHTTP(url=mcp.url))
                else:
                    mcp_servers.append(
                        MCPServerStdio(
                            command=mcp.command,
                            args=mcp.args.split(',') if mcp.args is not None else None,
                            env=mcp.env if mcp.env is not None else None,
                        )
                    )

        if obj.provider == McpLLMProvider.deepseek:
            model = OpenAIModel(
                obj.model,
                provider=DeepSeekProvider(api_key=obj.key),
            )
        elif obj.provider == McpLLMProvider.anthropic:
            model = AnthropicModel(
                obj.model,
                provider=AnthropicProvider(api_key=obj.key),
            )
        elif obj.provider == McpLLMProvider.gemini:
            model = GeminiModel(
                obj.model,
                provider=GoogleGLAProvider(api_key=obj.key),
            )
        else:
            model = OpenAIModel(
                obj.model,
                provider=OpenAIProvider(
                    base_url=obj.base_url,
                    api_key=obj.key,
                ),
            )

        agent = Agent(model, mcp_servers=mcp_servers)

        async def stream_messages():  # noqa: ANN202
            try:
                async with agent.run_mcp_servers():
                    async with agent.run_stream(obj.prompt) as result:
                        async for text in result.stream():
                            yield TextPart(text).content.encode('utf-8') + b'\n'
            except Exception as e:
                log.error(e)
                yield response_base.fail(data=str(e)).model_dump_json()

        return stream_messages()


mcp_service: McpService = McpService()
