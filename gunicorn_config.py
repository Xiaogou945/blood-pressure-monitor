bind = "0.0.0.0:8080"  # 监听所有网络接口的8080端口
workers = 4  # 工作进程数，通常设置为 CPU 核心数的2-4倍
worker_class = "sync"  # 工作进程类型
timeout = 120  # 超时时间（秒）
keepalive = 5  # keep-alive 连接的时间

# 日志设置
accesslog = "-"  # 访问日志输出到标准输出
errorlog = "-"   # 错误日志输出到标准输出
loglevel = "info"

# 进程名称
proc_name = "blood_pressure_monitor"

# 优雅重启
graceful_timeout = 120
