"""
测试管理系统 - 主应用包

基于 BrowserStack Test Management API 设计的专业软件测试管理系统
使用 FastAPI + PostgreSQL + MongoDB 技术栈
"""
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env（与 start_server_postgres.py 共用）
_env_file = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_file.exists():
    load_dotenv(_env_file)
# type: ignore  MC8yOmFIVnBZMlhsaUpqbWxvYzZiVE5pZWc9PTpiOTQzMmFiMA==

__version__ = "1.0.0"
__author__ = "Test Management Team"
# pragma: no cover  MS8yOmFIVnBZMlhsaUpqbWxvYzZiVE5pZWc9PTpiOTQzMmFiMA==

