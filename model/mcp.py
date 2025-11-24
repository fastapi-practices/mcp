from sqlalchemy import JSON, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Mcp(Base):
    """MCP 服务器表"""

    __tablename__ = 'sys_mcp'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='MCP 名称')
    type: Mapped[int] = mapped_column(default=0, comment='MCP 类型（0stdio 1sse）')
    description: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='MCP 描述'
    )
    url: Mapped[str | None] = mapped_column(String(255), default=None, comment='远程 SSE 地址')
    command: Mapped[str | None] = mapped_column(String(255), default=None, comment='MCP 命令')
    args: Mapped[str | None] = mapped_column(String(255), default=None, comment='MCP 命令参数')
    env: Mapped[str | None] = mapped_column(JSON(), default=None, comment='MCP 环境变量')
