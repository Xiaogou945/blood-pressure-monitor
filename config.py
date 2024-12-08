import os
from dotenv import load_dotenv
from urllib.parse import urlparse

# 在开发环境中加载.env文件
if os.path.exists('.env'):
    load_dotenv()

def get_safe_db_url(url):
    """安全地处理数据库 URL，移除敏感信息"""
    if not url:
        return None
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.hostname}"
    except Exception:
        return None

class Config:
    # 基本配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-this')
    
    # 构建数据库URL
    if os.getenv('POSTGRES_URL_NON_POOLING'):  # Vercel 推荐使用非连接池 URL
        SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL_NON_POOLING')
    elif os.getenv('POSTGRES_URL'):  # 备选：使用普通的 PostgreSQL URL
        SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL')
    else:
        # 从各个组件构建数据库URL
        db_user = os.getenv('POSTGRES_USER')
        db_password = os.getenv('POSTGRES_PASSWORD')
        db_host = os.getenv('POSTGRES_HOST')
        db_name = os.getenv('POSTGRES_DATABASE')
        
        if all([db_user, db_password, db_host, db_name]):
            SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
            if 'aws.neon.tech' in db_host:  # Neon 数据库需要 SSL
                SQLALCHEMY_DATABASE_URI += "?sslmode=require"
        else:
            # 如果环境变量不完整，使用SQLite作为后备
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 1,  # 最小连接数
        'max_overflow': 0,  # 最大溢出连接数
        'pool_timeout': 30,  # 连接超时时间（秒）
        'pool_recycle': 1800,  # 连接回收时间（秒）
    }
    
    # 打印实际使用的数据库URL（删除敏感信息）
    @classmethod
    def log_config(cls):
        db_url = cls.SQLALCHEMY_DATABASE_URI
        safe_url = get_safe_db_url(db_url)
        if safe_url:
            print(f"使用数据库: {safe_url}")
        else:
            print("使用SQLite数据库")
