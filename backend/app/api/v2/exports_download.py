"""
导出文件下载 API

提供 Agent 导出的 Excel 文件下载端点。
通过 MinIO 存储和下发，避免 Docker 内部地址和签名问题。
"""

import logging
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.config.minio_client import MinIOClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exports", tags=["导出下载"])


@router.get("/download/{filename:path}")
async def download_export_file(filename: str):
    """从 MinIO 下载 Agent 导出的 Excel 文件"""
    object_name = f"exports/{filename}"

    try:
        # 从 MinIO 获取文件内容
        data = MinIOClient.download_file(object_name=object_name)
    except Exception as e:
        logger.warning(f"MinIO 下载失败: {e}")
        raise HTTPException(status_code=404, detail=f"文件不存在: {filename}")

    # 使用 RFC 5987 编码支持中文文件名
    encoded_filename = quote(filename, safe="")
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
            "Content-Length": str(len(data)),
        },
    )
