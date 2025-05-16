#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field, HttpUrl

from backend.common.schema import SchemaBase
from backend.plugin.mcp.enums import McpLLMProvider, McpType


class McpSchemaBase(SchemaBase):
    name: str = Field(description='MCP 名称')
    type: McpType = Field(McpType.stdio, description='MCP 类型')
    description: str | None = Field(None, description='MCP 描述')
    url: HttpUrl | None = Field(None, description='远程 SSE 地址')
    command: str | None = Field(None, description='MCP 命令')
    args: str | None = Field(None, description='MCP 命令参数，多个参数用英文逗号隔开')
    env: dict[str, Any] | None = Field(None, description='MCP 环境变量')


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


class McpChatParam(SchemaBase):
    pk: list[int] = Field(description='MCP ID 列表')
    provider: McpLLMProvider = Field(McpLLMProvider.openai, description='LLM 供应商')
    model: str = Field(description='LLM 名称')
    key: str = Field(description='LLM API Key')
    base_url: str | None = Field(None, description='自定义 LLM API 地址，必须兼容 openai 供应商')
    prompt: str = Field(description='用户提示词')
