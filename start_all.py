#!/usr/bin/env python3
"""
一键启动所有服务：
  1. 大模型层 (LangGraph)  — 端口 2026
  2. 后台 (FastAPI)        — 端口 3001
  3. 前端 (Next.js)        — 端口 3000
  4. GitNexus              — 端口 5173

用法：
  1. 激活虚拟环境: .venv\Scripts\activate
  2. 运行本脚本:   python start_all.py
"""

import os
import sys
import subprocess
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_ACTIVATE = os.path.join(ROOT, ".venv", "Scripts", "activate.bat")
PYTHON = os.path.join(ROOT, ".venv", "Scripts", "python.exe")


def check_prerequisites():
    """检查前置条件"""
    errors = []

    # 检查虚拟环境
    if not os.path.exists(PYTHON):
        errors.append(f"虚拟环境 Python 不存在: {PYTHON}\n  请先运行: python -m venv .venv")
    if not os.path.exists(VENV_ACTIVATE):
        errors.append(f"虚拟环境激活脚本不存在: {VENV_ACTIVATE}\n  请先运行: python -m venv .venv")

    # 检查前端依赖
    if not os.path.exists(os.path.join(ROOT, "ui", "node_modules")):
        errors.append(f"前端依赖未安装\n  请运行: cd ui && npm install")

    # 检查 GitNexus 依赖
    if not os.path.exists(os.path.join(ROOT, "gitnexus-web", "node_modules")):
        errors.append(f"GitNexus 依赖未安装\n  请运行: cd gitnexus-web && npm install")

    if errors:
        print("=" * 55)
        print("  前置条件检查失败：")
        print()
        for err in errors:
            print(f"  ❌ {err}")
        print()
        print("  请解决以上问题后重试")
        print("=" * 55)
        sys.exit(1)


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

    check_prerequisites()

    # 1. 大模型层 (LangGraph)
    print("[1/4] 大模型层 (LangGraph) — http://localhost:2026")
    start_server(
        "LangGraph Server",
        f'"{PYTHON}" start_server_postgres.py',
        use_venv=True,
    )
    time.sleep(5)

    # 2. 后台 (FastAPI)
    print("[2/4] 后台 (FastAPI) — http://localhost:3001/docs")
    start_server(
        "Backend",
        f'"{PYTHON}" -m app.main',
        cwd=os.path.join(ROOT, "backend"),
        use_venv=True,
    )
    time.sleep(3)

    # 3. 前端 (Next.js)
    print("[3/4] 前端 (Next.js) — http://localhost:3000")
    start_server(
        "Frontend",
        "npm run dev",
        cwd=os.path.join(ROOT, "ui"),
    )
    time.sleep(3)

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
