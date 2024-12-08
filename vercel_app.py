import os
from flask import Flask
from app import app, db
import logging
from config import Config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        # 记录数据库配置信息
        Config.log_config()
        
        with app.app_context():
            db.create_all()
            logger.info("Database initialized successfully")
            
            # 测试数据库连接
            db.session.execute('SELECT 1')
            logger.info("Database connection test successful")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

try:
    # Initialize the database when the application starts
    init_db()
    logger.info("Application initialized successfully")
except Exception as e:
    logger.error(f"Application initialization failed: {str(e)}")
    raise

# Vercel expects an "app" object
application = app
