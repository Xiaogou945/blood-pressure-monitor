import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 在生产环境中，应该使用环境变量设置这些值
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-this')
    
    # 使用 PostgreSQL 数据库
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL', 'sqlite:///:memory:')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
