#!/usr/bin/env python3
"""启动 LightRAG API 服务器"""
import os
import sys

# 设置 UTF-8 环境
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 切换到 LightRAG 目录
os.chdir(r"D:\work\codes\ai_codes\tmp\2026-06-10-ai-test-agent-system-platform\ai-test-agent-system-platform\rag-example\2026-04-11-anything-chat-rag\anything-chat-rag")

from lightrag.api.lightrag_server import main

if __name__ == "__main__":
    main()
