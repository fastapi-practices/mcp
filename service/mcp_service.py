from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.mcp.crud.crud_mcp import mcp_dao
from backend.plugin.mcp.model import Mcp
from backend.plugin.mcp.schema.mcp import CreateMcpParam, UpdateMcpParam


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


mcp_service: McpService = McpService()
