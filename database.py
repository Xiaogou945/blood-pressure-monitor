import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# 配置日志
logger = logging.getLogger(__name__)

# 创建数据库实例
db = SQLAlchemy()

class BloodPressure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    systolic = db.Column(db.Integer, nullable=False)  # 收缩压
    diastolic = db.Column(db.Integer, nullable=False)  # 舒张压
    measure_date = db.Column(db.Date, nullable=False)  # 测量日期
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    note = db.Column(db.String(200))

def test_db_connection(app):
    """测试数据库连接"""
    try:
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()
        connection.close()
        logger.info("数据库连接测试成功")
        return True
    except SQLAlchemyError as e:
        logger.error(f"数据库连接测试失败: {str(e)}")
        return False

def init_app(app):
    """初始化数据库"""
    try:
        # 测试数据库连接
        if not test_db_connection(app):
            raise Exception("数据库连接失败")
        
        # 初始化 SQLAlchemy
        db.init_app(app)
        
        # 确保所有表都存在
        with app.app_context():
            db.create_all()
            logger.info("数据库表创建成功")
            
        return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        return False
