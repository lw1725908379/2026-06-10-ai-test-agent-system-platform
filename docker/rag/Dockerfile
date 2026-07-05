FROM python:3.12

WORKDIR /app

# 使用国内镜像源
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list 2>/dev/null || true

# 安装系统依赖
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 复制所有项目文件后再安装（避免动态版本读取问题）
COPY rag /app/rag

# 安装基础依赖
RUN pip install --no-cache-dir fastapi uvicorn pydantic-settings python-dotenv httpx

# 手动安装所有API依赖（不使用editable模式，避免版本解析问题）
RUN pip install --no-cache-dir \
    aiohttp \
    configparser \
    json_repair \
    nano-vectordb \
    networkx \
    "numpy>=1.24.0,<3.0.0" \
    "openai>=2.0.0,<3.0.0" \
    "pandas>=2.0.0,<2.4.0" \
    pipmaster \
    pydantic \
    pypinyin \
    python-dotenv \
    setuptools \
    tenacity \
    tiktoken \
    xlsxwriter \
    "google-api-core>=2.0.0,<3.0.0" \
    "google-genai>=1.0.0,<2.0.0" \
    aiofiles \
    ascii_colors \
    distro \
    httpcore \
    "httpx>=0.28.1" \
    jiter \
    "bcrypt>=4.0.0" \
    psutil \
    "PyJWT>=2.8.0,<3.0.0" \
    "python-jose[cryptography]" \
    python-multipart \
    pytz \
    gunicorn \
    "openpyxl>=3.0.0,<4.0.0" \
    pycryptodome \
    "pypdf>=6.1.0" \
    "python-docx>=0.8.11,<2.0.0" \
    "python-pptx>=0.6.21,<2.0.0"

# 安装 raganything
RUN pip install --no-cache-dir raganything

# 返回工作目录
WORKDIR /app

# 创建目录
RUN mkdir -p /app/storage /app/inputs

# 复制 .env 文件
COPY rag/.env /app/.env

# 复制启动脚本
COPY docker/rag/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 设置 PYTHONPATH 和环境变量
ENV PYTHONPATH=/app/rag/api
ENV LIGHTRAG_RUNTIME_TARGET=docker

EXPOSE 9623

# 直接执行入口脚本
CMD ["/bin/bash", "/app/entrypoint.sh"]
