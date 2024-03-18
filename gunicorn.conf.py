import os
from dotenv import load_dotenv

for env_file in ('.env', '.flaskenv'):
    env = os.path.join(os.getcwd(), env_file)
    print(env)
    if os.path.exists(env):
        load_dotenv(env)

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