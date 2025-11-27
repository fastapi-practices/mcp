from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.mcp.api.v1.mcp import router as mcp_router

v1 = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

v1.include_router(mcp_router, prefix='/mcps', tags=['MCP'])
