# gunicorn.conf.py
# Non logging stuff
bind = "0.0.0.0:8000"
workers = 1
threads = 2
# Access log - records incoming HTTP requests
accesslog = "-"
# Error log - records Gunicorn server goings-on
errorlog = "-"
# How verbose the Gunicorn error logs should be 
loglevel = "info"