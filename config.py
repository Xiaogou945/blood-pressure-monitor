import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 在生产环境中，应该使用环境变量设置这些值
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-this')
    
    # Vercel 环境下使用 SQLite 内存数据库
    # 注意：由于 Vercel 的无服务器特性，数据不会持久化
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
