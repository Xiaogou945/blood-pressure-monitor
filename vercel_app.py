import os
import sys
from flask import Flask, jsonify
from app import app
from database import db, init_app
import logging
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if os.getenv('DEBUG') == 'true' else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_environment():
    """Log important environment variables"""
    env_vars = [
        'FLASK_ENV', 'FLASK_APP', 'PYTHONPATH', 'POSTGRES_URL',
        'POSTGRES_HOST', 'POSTGRES_DATABASE'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if var in ['POSTGRES_URL']:  # 敏感信息不要完整记录
            logger.info(f"{var} is {'set' if value else 'not set'}")
        else:
            logger.info(f"{var}: {value}")

def init_database():
    try:
        # 记录环境信息
        log_environment()
        
        # 记录数据库配置信息
        Config.log_config()
        
        # 测试数据库连接
        try:
            with app.app_context():
                db.session.execute('SELECT 1')
                logger.info("Database connection test successful")
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            raise
            
        # 初始化数据库
        try:
            init_app(app)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise
            
    except Exception as e:
        logger.error(f"Error in database initialization: {str(e)}")
        logger.error(f"Python version: {sys.version}")
        raise

@app.errorhandler(500)
def handle_500_error(error):
    logger.error(f"Internal Server Error: {str(error)}")
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

try:
    # Initialize the database when the application starts
    init_database()
    logger.info("Application initialized successfully")
except Exception as e:
    logger.error(f"Application initialization failed: {str(e)}")
    # 在开发环境中重新抛出异常，在生产环境中继续运行
    if os.getenv('FLASK_ENV') != 'production':
        raise

# Vercel expects an "app" object
application = app
