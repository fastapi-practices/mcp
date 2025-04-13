#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from starlette.responses import StreamingResponse

from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession
from backend.plugin.mcp.schema.mcp import CreateMcpParam, GetMcpDetail, McpChatParam, UpdateMcpParam
from backend.plugin.mcp.service.mcp_service import mcp_service

router = APIRouter()


@router.get('/{pk}', summary='获取 MCP 服务器详情', dependencies=[DependsJwtAuth])
async def get_mcp(pk: Annotated[int, Path(description='MCP ID')]) -> ResponseSchemaModel[GetMcpDetail]:
    mcp = await mcp_service.get(pk=pk)
    return response_base.success(data=mcp)


@router.get(
    '',
    summary='分页获取所有 MCP 服务器',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_mcps(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='MCP 名称')] = None,
    type: Annotated[int | None, Query(description='MCP 类型')] = None,
) -> ResponseSchemaModel[PageData[GetMcpDetail]]:
    mcp_select = await mcp_service.get_select(name=name, type=type)
    page_data = await paging_data(db, mcp_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建 MCP 服务器',
    dependencies=[
        Depends(RequestPermission('sys:mcp:add')),
        DependsRBAC,
    ],
)
async def create_mcp(obj: CreateMcpParam) -> ResponseModel:
    await mcp_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新 MCP 服务器',
    dependencies=[
        Depends(RequestPermission('sys:mcp:edit')),
        DependsRBAC,
    ],
)
async def update_mcp(pk: Annotated[int, Path(description='MCP ID')], obj: UpdateMcpParam) -> ResponseModel:
    count = await mcp_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除 MCP 服务器',
    dependencies=[
        Depends(RequestPermission('sys:mcp:del')),
        DependsRBAC,
    ],
)
async def delete_mcp(pk: Annotated[int, Path(description='MCP ID')]) -> ResponseModel:
    count = await mcp_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.post(
    '/chat',
    summary='MCP ChatGPT',
    dependencies=[
        Depends(RequestPermission('sys:mcp:run')),
        DependsRBAC,
    ],
)
async def mcp_chat(obj: McpChatParam) -> StreamingResponse:
    data = await mcp_service.chat(obj=obj)
    return StreamingResponse(data, media_type='text/event-stream')
