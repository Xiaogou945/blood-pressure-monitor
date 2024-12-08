import os
from flask import Flask
from app import app, db
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database initialized successfully")
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
