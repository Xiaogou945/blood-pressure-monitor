import os
import sys
from flask import Flask

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vercel_app import app

def handler(request):
    """处理 HTTP 请求的 serverless 函数"""
    with app.request_context(request):
        try:
            return app.full_dispatch_request()
        except Exception as e:
            app.logger.error(f"请求处理错误: {str(e)}")
            return str(e), 500
