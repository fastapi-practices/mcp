from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.mcp.model import Mcp
from backend.plugin.mcp.schema.mcp import CreateMcpParam, UpdateMcpParam


class CRUDMcp(CRUDPlus[Mcp]):
    """MCP 服务器数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> Mcp | None:
        """
        获取 MCP 服务器

        :param db: 数据库会话
        :param pk: MCP ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> Mcp | None:
        """
        通过名称获取 MCP 服务器

        :param db: 数据库会话
        :param name: MCP 名称
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def get_list(self, name: str | None, type: int | None) -> Select[Mcp]:
        """
        获取 MCP 服务器列表

        :param name: MCP 名称
        :param type: MCP 类型
        :return:
        """
        filters = {}
        if name is not None:
            filters.update(name__like=f'%{name}%')
        if type is not None:
            filters.update(type=type)
        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateMcpParam) -> None:
        """
        创建 MCP 服务器

        :param db: 数据库会话
        :param obj: 创建 MCP 服务器参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateMcpParam) -> int:
        """
        更新 MCP 服务器

        :param db: 数据库会话
        :param pk: MCP ID
        :param obj: 更新 MCP 服务器参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        删除 MCP 服务器

        :param db: 数据库会话
        :param pk: MCP ID
        :return:
        """
        return await self.delete_model(db, pk)


mcp_dao: CRUDMcp = CRUDMcp(Mcp)
