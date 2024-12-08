import unittest
from datetime import datetime, date
from app import app, db, BloodPressure

class BloodPressureTests(unittest.TestCase):
    def setUp(self):
        # 配置测试数据库
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # 创建测试数据库和表
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        # 清理测试数据库
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_add_normal_bp(self):
        """测试添加正常范围的血压值"""
        data = {
            'systolic': 120,  # 正常收缩压
            'diastolic': 80,  # 正常舒张压
            'measure_date': '2024-12-08',
            'note': '正常血压测试'
        }
        response = self.client.post('/add_record', json=data)
        self.assertEqual(response.status_code, 200)
        
        # 验证数据是否正确保存
        with app.app_context():
            bp = BloodPressure.query.first()
            self.assertEqual(bp.systolic, 120)
            self.assertEqual(bp.diastolic, 80)
    
    def test_add_high_bp(self):
        """测试添加高血压值"""
        data = {
            'systolic': 145,  # 高收缩压
            'diastolic': 95,  # 高舒张压
            'measure_date': '2024-12-08',
            'note': '高血压测试'
        }
        response = self.client.post('/add_record', json=data)
        self.assertEqual(response.status_code, 200)
    
    def test_add_low_bp(self):
        """测试添加低血压值"""
        data = {
            'systolic': 85,  # 低收缩压
            'diastolic': 55,  # 低舒张压
            'measure_date': '2024-12-08',
            'note': '低血压测试'
        }
        response = self.client.post('/add_record', json=data)
        self.assertEqual(response.status_code, 200)
    
    def test_add_boundary_bp(self):
        """测试添加边界值"""
        data = {
            'systolic': 140,  # 收缩压警戒线
            'diastolic': 85,  # 舒张压警戒线
            'measure_date': '2024-12-08',
            'note': '边界值测试'
        }
        response = self.client.post('/add_record', json=data)
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_bp(self):
        """测试无效的血压值"""
        # 测试负值
        data = {
            'systolic': -120,
            'diastolic': -80,
            'measure_date': '2024-12-08'
        }
        response = self.client.post('/add_record', json=data)
        self.assertEqual(response.status_code, 400)
        
        # 测试异常高值
        data = {
            'systolic': 300,
            'diastolic': 200,
            'measure_date': '2024-12-08'
        }
        response = self.client.post('/add_record', json=data)
        self.assertEqual(response.status_code, 400)
    
    def test_get_data(self):
        """测试获取血压数据"""
        # 添加测试数据
        with app.app_context():
            test_data = [
                BloodPressure(
                    systolic=120,
                    diastolic=80,
                    measure_date=date(2024, 12, 1),
                    timestamp=datetime.now(),
                    note='测试数据1'
                ),
                BloodPressure(
                    systolic=145,
                    diastolic=95,
                    measure_date=date(2024, 12, 2),
                    timestamp=datetime.now(),
                    note='测试数据2'
                ),
                BloodPressure(
                    systolic=85,
                    diastolic=55,
                    measure_date=date(2024, 12, 3),
                    timestamp=datetime.now(),
                    note='测试数据3'
                )
            ]
            db.session.add_all(test_data)
            db.session.commit()
        
        # 测试获取所有数据
        response = self.client.get('/get_data')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        # 验证返回了7天的数据点（包括空值）
        self.assertEqual(len(data['systolic']), 7)
        self.assertEqual(len(data['diastolic']), 7)
        
        # 验证实际数据值
        actual_values = [x for x in data['systolic'] if x is not None]
        self.assertEqual(len(actual_values), 2)  # 只有2天的数据在查询范围内
        
        # 验证最新的数据点
        self.assertEqual(data['systolic'][0], 145)  # 12月2日的收缩压
        self.assertEqual(data['diastolic'][0], 95)  # 12月2日的舒张压

if __name__ == '__main__':
    unittest.main()
