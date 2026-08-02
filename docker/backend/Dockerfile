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

# 复制项目根目录的依赖文件
COPY pyproject.toml uv.lock ./

# 安装项目依赖
RUN uv sync --frozen --no-cache

# 复制 backend 代码
COPY backend/ /app/backend/
COPY .env /app/backend/.env

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/backend

EXPOSE 3001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]
