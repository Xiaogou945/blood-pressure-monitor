from flask import Flask, request, jsonify, render_template
from datetime import datetime, date, timedelta
import pandas as pd
from config import Config
from database import db, BloodPressure, init_app

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
init_app(app)

def analyze_blood_pressure(systolic, diastolic):
    # 血压分析标准（根据中国高血压防治指南）
    status = ""
    advice = ""
    
    if systolic < 90 or diastolic < 60:
        status = "低血压"
        advice = "建议增加盐分摄入，保持充足休息，必要时咨询医生。"
    elif systolic < 120 and diastolic < 80:
        status = "理想血压"
        advice = "继续保持健康的生活方式。"
    elif systolic < 130 and diastolic < 85:
        status = "正常血压"
        advice = "保持当前的生活习惯，定期监测血压。"
    elif systolic < 140 and diastolic < 90:
        status = "正常高值"
        advice = "建议适当控制饮食，增加运动，定期监测血压。"
    else:
        status = "高血压"
        advice = "建议立即就医，遵医嘱服药，控制饮食，规律作息。"
    
    return status, advice

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    
    # 数据验证
    if not data or 'systolic' not in data or 'diastolic' not in data:
        return jsonify({'error': '缺少必要的血压数据'}), 400
    
    systolic = data.get('systolic')
    diastolic = data.get('diastolic')
    
    # 验证血压值的合理范围
    if not isinstance(systolic, (int, float)) or not isinstance(diastolic, (int, float)):
        return jsonify({'error': '血压值必须是数字'}), 400
    
    if systolic <= 0 or diastolic <= 0:
        return jsonify({'error': '血压值不能为负数或零'}), 400
    
    if systolic > 250 or diastolic > 150:
        return jsonify({'error': '血压值超出正常范围'}), 400
    
    # 处理日期
    measure_date = data.get('measure_date')
    if measure_date:
        try:
            measure_date = datetime.strptime(measure_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': '日期格式无效'}), 400
    else:
        measure_date = datetime.now().date()
    
    # 创建记录
    bp = BloodPressure(
        systolic=systolic,
        diastolic=diastolic,
        measure_date=measure_date,
        timestamp=datetime.now(),
        note=data.get('note', '')
    )
    
    try:
        db.session.add(bp)
        db.session.commit()
        status, advice = analyze_blood_pressure(systolic, diastolic)
        return jsonify({
            'message': '记录添加成功',
            'status': status,
            'advice': advice
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '保存记录失败'}), 500

@app.route('/get_data')
def get_data():
    period = request.args.get('period', 'week')
    
    # 获取当前日期
    today = datetime.now().date()
    
    # 根据时间段设置查询范围
    if period == 'week':
        start_date = today - timedelta(days=6)  # 显示最近7天（包括今天）
    elif period == 'month':
        start_date = today - timedelta(days=29)  # 显示最近30天（包括今天）
    elif period == 'year':
        start_date = today - timedelta(days=364)  # 显示最近365天（包括今天）
    else:
        start_date = today - timedelta(days=6)  # 默认显示最近7天
    
    print(f"Querying data from {start_date} to {today}")  # 调试信息
    
    # 查询指定时间范围内的记录
    records = BloodPressure.query.filter(
        BloodPressure.measure_date >= start_date,
        BloodPressure.measure_date <= today
    ).order_by(BloodPressure.measure_date.asc()).all()
    
    print(f"Found {len(records)} records")  # 调试信息
    
    if not records:
        return jsonify({
            'labels': [],
            'systolic': [],
            'diastolic': []
        })
    
    # 创建日期范围内的所有日期
    date_range = pd.date_range(start=start_date, end=today, freq='D')
    
    # 创建一个空的DataFrame，包含所有日期
    df = pd.DataFrame(index=date_range)
    df.index.name = 'date'
    
    # 添加血压数据
    data_dict = {r.measure_date: {'systolic': r.systolic, 'diastolic': r.diastolic} for r in records}
    
    # 填充数据
    df['systolic'] = df.index.map(lambda x: data_dict.get(x.date(), {}).get('systolic', None))
    df['diastolic'] = df.index.map(lambda x: data_dict.get(x.date(), {}).get('diastolic', None))
    
    print(f"DataFrame: {df.to_dict()}")  # 调试信息
    
    # 将数据转换为前端所需的格式
    data = {
        'labels': [d.strftime('%Y-%m-%d') for d in df.index],
        'systolic': [s if pd.notnull(s) else None for s in df['systolic']],
        'diastolic': [d if pd.notnull(d) else None for d in df['diastolic']]
    }
    
    print(f"Returning data: {data}")  # 调试信息
    
    return jsonify(data)

@app.route('/debug_data')
def debug_data():
    records = BloodPressure.query.order_by(BloodPressure.measure_date.desc()).all()
    data = [{
        'measure_date': record.measure_date.strftime('%Y-%m-%d'),
        'systolic': record.systolic,
        'diastolic': record.diastolic
    } for record in records]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
