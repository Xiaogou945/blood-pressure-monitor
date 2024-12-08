import os
import sys
import traceback
import logging
from flask import Flask, jsonify, current_app
from config import Config
from database import init_app, db, test_db_connection

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if os.getenv('DEBUG') == 'true' else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建应用
app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
if not init_app(app):
    logger.error("数据库初始化失败")
    raise Exception("数据库初始化失败")

def log_environment():
    """记录重要的环境变量"""
    env_vars = [
        'FLASK_ENV', 'FLASK_APP', 'PYTHONPATH', 'POSTGRES_URL',
        'POSTGRES_HOST', 'POSTGRES_DATABASE', 'PYTHON_VERSION'
    ]
    
    logger.info("当前环境变量：")
    for var in env_vars:
        value = os.getenv(var)
        if var in ['POSTGRES_URL']:  # 敏感信息不要完整记录
            logger.info(f"{var} 已设置: {'是' if value else '否'}")
            if value:
                logger.info(f"{var} 连接信息: {Config.get_safe_db_url(value)}")
        else:
            logger.info(f"{var}: {value}")
    
    logger.info(f"Python 版本: {sys.version}")
    logger.info(f"Python 路径: {sys.path}")

@app.route('/')
def home():
    return 'Blood Pressure Monitor API'

@app.route('/debug')
def debug():
    """返回调试信息的端点"""
    try:
        # 测试数据库连接
        db_status = test_db_connection(app)
        
        debug_info = {
            'python_version': sys.version,
            'env_vars': {k: v for k, v in os.environ.items() if not any(secret in k.lower() for secret in ['password', 'secret', 'key'])},
            'database_url': Config.get_safe_db_url(app.config['SQLALCHEMY_DATABASE_URI']),
            'database_status': db_status
        }
        return jsonify(debug_info)
    except Exception as e:
        current_app.logger.error(f"调试端点错误: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.errorhandler(Exception)
def handle_error(error):
    """全局错误处理器"""
    current_app.logger.error(f"未处理的异常: {str(error)}\n{traceback.format_exc()}")
    return jsonify({
        'error': str(error),
        'type': error.__class__.__name__
    }), 500

if __name__ == '__main__':
    log_environment()
    app.run(debug=True)
