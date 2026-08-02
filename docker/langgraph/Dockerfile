FROM python:3.12-slim

WORKDIR /app

# 安装 Node.js 20（Playwright 测试运行需要 node/npx）
# 注意：必须在容器内持久安装，不能依赖运行时 apt-get（容器重建会丢失）
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && node --version && npm --version

# 安装 uv
RUN pip install uv --no-cache-dir

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装项目依赖
RUN uv sync --frozen --no-cache

# 安装 Playwright 及 Chromium 浏览器（持久化，避免运行时下载）
# 浏览器安装在 /root/.cache/ms-playwright，容器重建后仍保留
RUN npm install -g playwright@1.62.1 \
    && npx playwright install chromium --with-deps \
    && rm -rf /root/.npm/_cacache

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
