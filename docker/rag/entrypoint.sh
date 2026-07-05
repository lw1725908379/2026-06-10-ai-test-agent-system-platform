#!/bin/bash
set -e

# 设置 PYTHONPATH 和环境变量
export PYTHONPATH=/app/rag/api
export LIGHTRAG_RUNTIME_TARGET=docker

# 启动 LightRAG API
cd /app/rag
exec python -m lightrag.api.lightrag_server --host 0.0.0.0 --port 9623
