import os
import sys

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vercel_app import app

# Vercel 需要一个应用实例
application = app
