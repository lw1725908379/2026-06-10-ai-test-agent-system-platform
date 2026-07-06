"""
API 路由模块

包含所有 API 端点的路由定义
"""

from fastapi import APIRouter
# pragma: no cover  MC8yOmFIVnBZMlhsaUpqbWxvYzZkSGx0UWc9PTo1Nzk1OTU0Mw==

from .v2 import projects, folders, test_cases, test_runs, test_results, attachments, configurations, test_plans, documents, api_tests, api_tests_extended, api_endpoints, scenarios, web_tests, web_functions, pentests, mcp_proxy, android_tests, ai, exports_download

# 创建 API v2 路由
api_router = APIRouter(prefix="/api/v2")
# noqa  MS8yOmFIVnBZMlhsaUpqbWxvYzZkSGx0UWc9PTo1Nzk1OTU0Mw==

# 注册子路由
api_router.include_router(projects.router, tags=["项目管理"])
api_router.include_router(folders.router, tags=["文件夹管理"])
api_router.include_router(test_cases.router, tags=["测试用例管理"])
api_router.include_router(test_cases.exports_router, tags=["导出管理"])
api_router.include_router(test_plans.router, tags=["测试计划管理"])
api_router.include_router(test_runs.router, tags=["测试运行管理"])
api_router.include_router(test_results.router, tags=["测试结果管理"])
api_router.include_router(attachments.test_case_attachments_router, tags=["附件管理"])
api_router.include_router(attachments.test_result_attachments_router, tags=["附件管理"])
api_router.include_router(attachments.attachments_router, tags=["附件管理"])
api_router.include_router(configurations.router, tags=["配置管理"])
api_router.include_router(documents.router, tags=["文档管理"])
api_router.include_router(api_tests.router, tags=["API 测试管理"])
api_router.include_router(api_tests_extended.router, tags=["API 测试扩展"])
api_router.include_router(api_endpoints.router, tags=["API 端点管理"])
api_router.include_router(scenarios.router, prefix="/scenarios", tags=["场景测试管理"])
api_router.include_router(web_tests.router, tags=["Web 测试管理"])
api_router.include_router(web_functions.router, tags=["Web 功能管理"])
api_router.include_router(android_tests.router, tags=["Android 测试管理"])
api_router.include_router(android_tests.devices_router, tags=["Android 设备管理"])
api_router.include_router(pentests.router, tags=["渗透测试管理"])
api_router.include_router(mcp_proxy.router, tags=["MCP 代理"])
api_router.include_router(ai.router, tags=["AI 辅助"])
api_router.include_router(exports_download.router, tags=["导出下载"])

__all__ = ["api_router"]
