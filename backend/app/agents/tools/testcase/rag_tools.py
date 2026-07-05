"""
RAG 查询工具 — 直接调用 RAG API，不依赖 MCP 客户端

提供知识库检索工具供 Agent 使用，在模块加载时直接创建，无异步依赖。
"""

import json
import logging
from typing import List, Optional

import httpx
from langchain_core.tools import BaseTool, tool

from app.config.settings import settings

logger = logging.getLogger(__name__)


@tool
async def rag_query_data(
    query: str,
    mode: str = "mix",
    top_k: int = 60,
) -> str:
    """从知识库检索结构化数据：实体、关系、文本块和引用来源。

    返回 JSON 格式的结构化检索结果，适合程序化处理。
    当需要获取知识图谱中的实体关系信息（而非LLM生成的回答）时使用此工具。

    参数：
        query: 自然语言查询
        mode: 检索模式（mix推荐, local, global, hybrid, naive）
        top_k: 检索的实体/关系数量
    """
    try:
        url = f"{settings.rag_api_url}/query/data"
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                url,
                json={
                    "query": query,
                    "mode": mode,
                    "top_k": top_k,
                },
            )
            resp.raise_for_status()
            return resp.text
    except Exception as e:
        logger.warning(f"RAG query failed: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@tool
async def rag_query(
    query: str,
    mode: str = "hybrid",
) -> str:
    """从知识库查询信息并生成回答。

    返回 LLM 生成的回答及引用来源。
    当需要获取可读的自然语言回答时使用此工具。

    参数：
        query: 自然语言查询
        mode: 检索模式（hybrid推荐, local, global, naive）
    """
    try:
        url = f"{settings.rag_api_url}/query"
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                url,
                json={
                    "query": query,
                    "mode": mode,
                },
            )
            resp.raise_for_status()
            return resp.text
    except Exception as e:
        logger.warning(f"RAG query failed: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@tool
async def rag_graph_search(
    query: str,
) -> str:
    """在知识图谱中搜索实体。

    参数：
        query: 实体名称或关键词
    """
    try:
        url = f"{settings.rag_api_url}/graph/label/search"
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                url,
                params={"query": query},
            )
            resp.raise_for_status()
            return resp.text
    except Exception as e:
        logger.warning(f"RAG graph search failed: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@tool
async def rag_graph_get(
    label: str,
) -> str:
    """获取知识图谱中指定实体周围的子图信息。

    参数：
        label: 实体标签名称
    """
    try:
        url = f"{settings.rag_api_url}/graphs"
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                url,
                params={"label": label},
            )
            resp.raise_for_status()
            return resp.text
    except Exception as e:
        logger.warning(f"RAG graph get failed: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def build_rag_tools() -> List[BaseTool]:
    """构建 RAG 工具列表。

    在模块加载时直接创建，无异步/网络依赖。
    RAG API 调用发生在工具执行时，而非创建时。
    """
    return [
        rag_query_data,
        rag_query,
        rag_graph_search,
        rag_graph_get,
    ]
