import os
import sys

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vercel_app import app

# Vercel 需要一个 WSGI 处理函数
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

# 同时保留应用实例以兼容其他 WSGI 服务器
application = app
