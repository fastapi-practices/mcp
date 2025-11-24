from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field, HttpUrl, Json

from backend.common.schema import SchemaBase
from backend.plugin.mcp.enums import McpType


class McpSchemaBase(SchemaBase):
    name: str = Field(description='MCP 名称')
    type: McpType = Field(McpType.stdio, description='MCP 类型')
    description: str | None = Field(None, description='MCP 描述')
    url: HttpUrl | None = Field(None, description='MCP 服务器端点链接')
    headers: str | None = Field(None, description='请求 MCP 服务器端点时的请求头')
    command: str | None = Field(None, description='MCP 命令')
    args: Json[list[str]] | None = Field(None, description='MCP 命令参数')
    env: Json[dict[str, Any]] | None = Field(None, description='MCP 环境变量')
    timeout: float | None = Field(5, description='客户端初始化超时时间（秒）')
    read_timeout: float | None = Field(5 * 60, description='等待新消息的最长时间（秒）')


class CreateMcpParam(McpSchemaBase):
    """创建 MCP 服务器参数"""


class UpdateMcpParam(McpSchemaBase):
    """更新 MCP 服务器参数"""


class GetMcpDetail(McpSchemaBase):
    """MCP 服务器详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='MCP ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
