from backend.common.enums import IntEnum


class McpType(IntEnum):
    """Mcp 服务器类型"""

    stdio = 0
    sse = 1
    streamable_http = 2
