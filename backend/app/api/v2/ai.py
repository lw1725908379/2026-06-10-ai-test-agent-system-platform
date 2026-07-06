"""
AI 辅助功能 API 路由

提供 AI 辅助填充测试用例字段等功能。
"""

import json
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.llms import text_model

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projects/{project_id}/ai", tags=["AI 辅助"])


class AssistFieldContext(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    preconditions: Optional[str] = None
    existing_steps: Optional[list[dict]] = None


class AIAssistFieldRequest(BaseModel):
    field: str  # "description" | "preconditions" | "steps"
    context: AssistFieldContext
    prompt: Optional[str] = None


class AIAssistFieldResponse(BaseModel):
    success: bool
    content: str | list[dict]
    message: Optional[str] = None


_PROMPT_TEMPLATES = {
    "description": """你是一位资深测试工程师。基于以下测试用例信息，生成一段专业、完整的测试用例描述（不超过200字）。

测试用例标题：{title}
已有描述：{description}
前置条件：{preconditions}

要求：
- 描述测试目的和验证范围
- 语言简洁专业
- 直接返回描述文本，不要多余的解释""",

    "preconditions": """你是一位资深测试工程师。基于以下测试用例信息，生成前置条件。

测试用例标题：{title}
用例描述：{description}

要求：
- 列出执行此用例前必须满足的条件
- 每条条件独立一行，用数字编号
- 直接返回前置条件文本，不要多余的解释""",

    "steps": """你是一位资深测试工程师。基于以下测试用例信息，生成详细的测试步骤和预期结果。

测试用例标题：{title}
用例描述：{description}
前置条件：{preconditions}

要求：
- 生成 3-6 条测试步骤
- 每条步骤包含「步骤描述」和「预期结果」
- 覆盖正常流程和边界情况
- 以 JSON 数组格式返回，不要多余的解释，格式：
[{{"step": "步骤描述", "result": "预期结果"}}]""",
}


@router.post("/assist-field", response_model=AIAssistFieldResponse)
async def assist_field(project_id: str, request: AIAssistFieldRequest):
    """AI 辅助填充测试用例字段"""
    try:
        # 字段校验
        if request.field not in _PROMPT_TEMPLATES:
            raise HTTPException(status_code=400, detail=f"不支持的字段: {request.field}")

        # 构建提示词
        prompt_template = _PROMPT_TEMPLATES[request.field]
        prompt = prompt_template.format(
            title=request.context.title or "",
            description=request.context.description or "",
            preconditions=request.context.preconditions or "",
        )

        # 如果有自定义 prompt，追加
        if request.prompt:
            prompt += f"\n\n额外要求：{request.prompt}"

        # 调用 LLM
        response = await text_model.ainvoke(prompt)
        content = response.content.strip() if hasattr(response, "content") else str(response).strip()

        # steps 字段需要解析 JSON
        if request.field == "steps":
            try:
                parsed = json.loads(content)
                if isinstance(parsed, list):
                    return AIAssistFieldResponse(success=True, content=parsed)
            except json.JSONDecodeError:
                # 尝试从 markdown code block 中提取
                import re
                match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
                if match:
                    parsed = json.loads(match.group(1))
                    if isinstance(parsed, list):
                        return AIAssistFieldResponse(success=True, content=parsed)
                # 如果还是解析失败，返回原始文本
                return AIAssistFieldResponse(
                    success=True,
                    content=[{"step": step.strip(), "result": ""} for step in content.split("\n") if step.strip()],
                )

        return AIAssistFieldResponse(success=True, content=content)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI assist field failed: {e}", exc_info=True)
        return AIAssistFieldResponse(
            success=False,
            content="",
            message=f"AI 辅助失败: {str(e)}",
        )
