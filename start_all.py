#!/usr/bin/env python3
"""
一键启动所有服务：
  1. 大模型层 (LangGraph)  — 端口 2026
  2. 后台 (FastAPI)        — 端口 3001
  3. 前端 (Next.js)        — 端口 3000
  4. GitNexus              — 端口 5173
"""

import os
import sys
import subprocess
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_ACTIVATE = os.path.join(ROOT, ".venv", "Scripts", "activate.bat")
PYTHON = os.path.join(ROOT, ".venv", "Scripts", "python.exe")


def start_server(title, cmd, cwd=None, use_venv=False):
    """在独立 cmd 窗口中启动一个服务"""
    if use_venv:
        full_cmd = f'"{VENV_ACTIVATE}" && {cmd}'
    else:
        full_cmd = cmd

    subprocess.Popen(
        f'start "{title}" cmd /k "{full_cmd}"',
        shell=True,
        cwd=cwd or ROOT,
    )
    print(f"  [{title}] 启动中...")


def main():
    print("=" * 55)
    print("  智能测试平台 — 一键启动")
    print("=" * 55)
    print()

    # 1. 大模型层 (LangGraph)
    print("[1/4] 大模型层 (LangGraph) — http://localhost:2026")
    start_server(
        "LangGraph Server",
        f'"{PYTHON}" start_server_postgres.py',
        use_venv=True,
    )
    time.sleep(2)

    # 2. 后台 (FastAPI)
    print("[2/4] 后台 (FastAPI) — http://localhost:3001/docs")
    start_server(
        "Backend",
        f'"{PYTHON}" -m app.main',
        cwd=os.path.join(ROOT, "backend"),
        use_venv=True,
    )
    time.sleep(2)

    # 3. 前端 (Next.js)
    print("[3/4] 前端 (Next.js) — http://localhost:3000")
    start_server(
        "Frontend",
        "npm run dev",
        cwd=os.path.join(ROOT, "ui"),
    )
    time.sleep(2)

    # 4. GitNexus
    print("[4/4] GitNexus — http://localhost:5173/gitnexus-web/")
    start_server(
        "GitNexus",
        "npm run dev",
        cwd=os.path.join(ROOT, "gitnexus-web"),
    )

    print()
    print("=" * 55)
    print("  所有服务已启动！")
    print()
    print("  前端:      http://localhost:3000")
    print("  GitNexus:  http://localhost:5173/gitnexus-web/")
    print("  后端 API:  http://localhost:3001/docs")
    print("  LangGraph: http://localhost:2026/ok")
    print()
    print("  每个服务在独立窗口中运行，关窗即停")
    print("=" * 55)


if __name__ == "__main__":
    main()
