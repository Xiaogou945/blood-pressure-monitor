import os
import sys
import traceback
from flask import Flask, jsonify, current_app
from app import app
from database import db, init_app
import logging
from config import Config
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if os.getenv('DEBUG') == 'true' else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_safe_db_url(url):
    """安全地处理数据库 URL，移除敏感信息"""
    if not url:
        return "未设置"
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.hostname}"
    except Exception:
        return "无效的URL格式"

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
                logger.info(f"{var} 连接信息: {get_safe_db_url(value)}")
        else:
            logger.info(f"{var}: {value}")
    
    logger.info(f"Python 版本: {sys.version}")
    logger.info(f"Python 路径: {sys.path}")

def init_database():
    try:
        # 记录环境信息
        log_environment()
        
        # 记录数据库配置信息
        Config.log_config()
        
        # 测试数据库连接
        try:
            with app.app_context():
                result = db.session.execute('SELECT 1').scalar()
                logger.info(f"数据库连接测试成功: {result}")
        except Exception as e:
            logger.error(f"数据库连接测试失败: {str(e)}")
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            raise
            
        # 初始化数据库
        try:
            init_app(app)
            logger.info("数据库初始化成功")
        except Exception as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            raise
            
    except Exception as e:
        logger.error(f"数据库初始化过程中出错: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        if os.getenv('FLASK_ENV') != 'production':
            raise
        return str(e)

@app.errorhandler(Exception)
def handle_exception(error):
    """处理所有未捕获的异常"""
    error_info = {
        "error": "服务器内部错误",
        "message": str(error),
        "type": error.__class__.__name__,
        "traceback": traceback.format_exc()
    }
    logger.error(f"未捕获的异常: {error_info}")
    return jsonify(error_info), 500

@app.route('/debug')
def debug():
    """调试端点，返回环境信息"""
    try:
        with app.app_context():
            db_url = Config.SQLALCHEMY_DATABASE_URI
            info = {
                "python_version": sys.version,
                "env_vars": {k: v for k, v in os.environ.items() if not k.lower().startswith('password')},
                "config": {
                    "database_type": "postgres" if db_url and "postgres" in db_url else "sqlite",
                    "debug_mode": current_app.debug,
                    "testing_mode": current_app.testing,
                    "database_url": get_safe_db_url(db_url)
                }
            }
            return jsonify(info)
    except Exception as e:
        logger.error(f"调试端点出错: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

# 初始化应用
init_error = init_database()
if init_error:
    logger.warning(f"应用初始化时出现警告: {init_error}")
else:
    logger.info("应用初始化成功")

# Vercel需要一个app对象
application = app
