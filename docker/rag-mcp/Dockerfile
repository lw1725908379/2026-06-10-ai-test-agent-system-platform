# RAG MCP Server Dockerfile
# 基于 Python 3.12 slim 镜像

FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖（添加容错）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    || true
RUN rm -rf /var/lib/apt/lists/* || true

# 安装 Python 依赖
RUN pip install --no-cache-dir fastmcp httpx pydantic-settings python-dotenv

# 复制 RAG MCP Server 代码
COPY rag/rag_server.py ./rag_server.py

# 暴露端口
EXPOSE 8003

# 启动命令
CMD ["python", "rag_server.py", "--rag-url", "http://rag-api:9623", "--username", "admin", "--password", "admin123", "--space-id", "cmp_space", "--port", "8003"]
