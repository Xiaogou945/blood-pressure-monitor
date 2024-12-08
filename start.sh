#!/bin/bash

# 激活虚拟环境（如果使用的话）
# source venv/bin/activate

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=production

# 使用 gunicorn 启动应用
/Users/superchang/Library/Python/3.9/bin/gunicorn --config gunicorn_config.py app:app
