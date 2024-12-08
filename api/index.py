from http.server import BaseHTTPRequestHandler
import os
import sys

# 添加项目根目录到 Python 路径
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from vercel_app import app

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        try:
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # 返回应用响应
            response = app.test_client().get(self.path)
            self.wfile.write(response.data)
            
        except Exception as e:
            # 错误处理
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(e).encode())
