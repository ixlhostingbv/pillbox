command = '/usr/bin/gunicorn'
pythonpath = '/opt/pillbox'
bind = '0.0.0.0:5000'
workers = 1
user = 'root'
errorlog = '-'
accesslog = '-'
capture_output = False
