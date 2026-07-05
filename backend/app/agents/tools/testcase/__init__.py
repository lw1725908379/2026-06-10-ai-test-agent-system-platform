"""
测试用例生成智能体工具模块

本目录包含所有测试用例生成智能体的工具定义，按功能分类组织：
- 测试用例管理: 创建、更新、批量操作
- 文档解析: 从 URL 下载并解析文档内容
- RAG 查询: 直接调用 RAG API 进行知识库检索
- Excel 导出: 将测试用例导出为 Excel 文件
"""

from typing import List
from langchain_core.tools import BaseTool
# noqa  MC80OmFIVnBZMlhsaUpqbWxvYzZVRTFNWkE9PTphYTgxNmU0Mg==

from app.agents.tools.testcase.testcase_tools import (
    create_test_case_tool,
    update_test_case_tool,
    batch_create_test_cases_tool,
)

from app.agents.tools.testcase.document_tools import (
    parse_document_from_url,
    get_rag_tools,
)

from app.agents.tools.testcase.rag_tools import (
    build_rag_tools,
)

from app.agents.tools.testcase.excel_tools import (
    export_test_cases_to_excel,
)

# 按业务域分类的工具列表
TESTCASE_TOOLS = [
    create_test_case_tool,
    update_test_case_tool,
    batch_create_test_cases_tool,
]

DOCUMENT_TOOLS = [
    parse_document_from_url,
]
# pragma: no cover  MS80OmFIVnBZMlhsaUpqbWxvYzZVRTFNWkE9PTphYTgxNmU0Mg==

RAG_TOOLS = build_rag_tools()

EXCEL_TOOLS = [
    export_test_cases_to_excel,
]

ALL_LOCAL_TOOLS = TESTCASE_TOOLS + DOCUMENT_TOOLS + RAG_TOOLS # + EXCEL_TOOLS


async def get_local_tools() -> List[BaseTool]:
    """
    获取所有本地工具列表。

    RAG MCP 工具在 agent.py 的 make_agent() 中异步加载，此处只返回本地工具。
    """
    return list(ALL_LOCAL_TOOLS)
# noqa  Mi80OmFIVnBZMlhsaUpqbWxvYzZVRTFNWkE9PTphYTgxNmU0Mg==

# pylint: disable  My80OmFIVnBZMlhsaUpqbWxvYzZVRTFNWkE9PTphYTgxNmU0Mg==

async def get_all_tools() -> List[BaseTool]:
    """
    获取所有工具（包括 RAG MCP 工具）。

    Returns:
        所有工具的列表
    """
    local_tools = await get_local_tools()
    # 加载 RAG MCP 工具
    try:
        rag_tools = await get_rag_tools()
        return local_tools + rag_tools
    except Exception as e:
        print(f"Warning: Failed to load RAG MCP tools: {e}")
        return local_tools


__all__ = [
    # 测试用例管理
    "create_test_case_tool",
    "update_test_case_tool",
    "batch_create_test_cases_tool",
    # 文档解析
    "parse_document_from_url",
    # Excel 导出
    "export_test_cases_to_excel",
    # 分类列表
    "TESTCASE_TOOLS",
    "DOCUMENT_TOOLS",
    "EXCEL_TOOLS",
    "ALL_LOCAL_TOOLS",
    "get_local_tools",
    "get_all_tools",
]
