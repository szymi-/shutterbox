from shutterbox.settings import LOGGING

workers = 1
keepalive = 30
worker_class = "uvicorn.workers.UvicornWorker"
bind = ["0.0.0.0:8080"]

accesslog = "-"
errorlog = "-"
loglevel = "info"
logconfig_dict = LOGGING

forwarded_allow_ips = "*"
