command = 'gunicorn'
bind = '0.0.0.0:8001'
workers = 3
user = 'root'
loglevel = 'info'
pythonpath='/vagrant/xbrowse'

# log to stdout
errorlog = '-'  
accesslog = '-'