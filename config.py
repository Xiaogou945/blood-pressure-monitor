import os
from dotenv import load_dotenv

# 在开发环境中加载.env文件
if os.path.exists('.env'):
    load_dotenv()

class Config:
    # 基本配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-this')
    
    # 构建数据库URL
    if os.getenv('POSTGRES_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL')
    else:
        # 从各个组件构建数据库URL
        db_user = os.getenv('POSTGRES_USER')
        db_password = os.getenv('POSTGRES_PASSWORD')
        db_host = os.getenv('POSTGRES_HOST')
        db_name = os.getenv('POSTGRES_DATABASE')
        
        if all([db_user, db_password, db_host, db_name]):
            SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}?sslmode=require"
        else:
            # 如果环境变量不完整，使用SQLite作为后备
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 打印实际使用的数据库URL（删除敏感信息）
    @classmethod
    def log_config(cls):
        db_url = cls.SQLALCHEMY_DATABASE_URI
        if 'postgres' in db_url:
            # 隐藏敏感信息
            print("Using PostgreSQL database")
        else:
            print("Using SQLite database")
