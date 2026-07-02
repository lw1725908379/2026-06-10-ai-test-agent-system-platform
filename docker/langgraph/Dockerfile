FROM python:3.12-slim

WORKDIR /app

# 安装 uv
RUN pip install uv --no-cache-dir

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装项目依赖
RUN uv sync --frozen --no-cache

# 复制项目代码
COPY start_server_postgres.py .
COPY langgraph.json .
COPY langgraph_api/ langgraph_api/
COPY langgraph_runtime_postgres/ langgraph_runtime_postgres/
COPY langgraph_source/ langgraph_source/
COPY backend/ backend/
COPY .env .env
COPY storage/ storage/
COPY langgraph_license/ langgraph_license/
COPY openapi.json .

# 设置 venv 到 PATH
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 2026

CMD ["python", "start_server_postgres.py"]
