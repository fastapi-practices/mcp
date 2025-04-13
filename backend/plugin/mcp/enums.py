#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.enums import IntEnum, StrEnum


class McpType(IntEnum):
    """Mcp 服务器类型"""

    stdio = 0
    sse = 1


class McpLLMProvider(StrEnum):
    """MCP 大语言模型供应商"""

    openai = 'openai'
    deepseek = 'deepseek'
    anthropic = 'anthropic'
    gemini = 'gemini'
