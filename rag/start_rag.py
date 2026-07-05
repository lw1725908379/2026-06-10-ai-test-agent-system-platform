#!/usr/bin/env python3
"""
LightRAG + RAG-Anything 启动脚本

用法:
    python start_rag.py              # 启动 RAG API (默认端口 9623)
    python start_rag.py --port 9623  # 指定端口
    python start_rag.py --help       # 查看更多选项

依赖安装:
    pip install numpy pandas aiohttp fastapi uvicorn pydantic-settings python-dotenv httpx
    pip install raganything
"""
import os
import sys

# 设置 UTF-8 编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 添加 rag/api 到 PYTHONPATH，使 lightrag 模块可被导入
rag_api_path = os.path.join(script_dir, "api")
if rag_api_path not in sys.path:
    sys.path.insert(0, rag_api_path)

# 导入并启动
from lightrag.api.lightrag_server import main

if __name__ == "__main__":
    # 默认端口 9623
    sys.argv = ['start_rag.py', '--host', '0.0.0.0', '--port', '9623']
    main()
