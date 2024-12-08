from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建数据库实例
db = SQLAlchemy()

class BloodPressure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    systolic = db.Column(db.Integer, nullable=False)  # 收缩压
    diastolic = db.Column(db.Integer, nullable=False)  # 舒张压
    measure_date = db.Column(db.Date, nullable=False)  # 测量日期
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    note = db.Column(db.String(200))

def init_app(app):
    """初始化数据库"""
    db.init_app(app)
    
    # 确保所有表都存在
    with app.app_context():
        db.create_all()
