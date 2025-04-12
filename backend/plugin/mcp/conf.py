#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.path_conf import BASE_PATH


class McpSettings(BaseSettings):
    """MCP 配置"""

    model_config = SettingsConfigDict(env_file=f'{BASE_PATH}/.env', env_file_encoding='utf-8', extra='ignore')

    # .env MCP
    MCP_OPENAI_API_KEY: str | None = None
    MCP_DEEPSEEK_API_KEY: str | None = None
    MCP_ANTHROPIC_API_KEY: str | None = None
    MCP_GEMINI_API_KEY: str | None = None


@lru_cache
def get_mcp_settings() -> McpSettings:
    """获取 MCP 配置"""
    return McpSettings()


mcp_settings = get_mcp_settings()
