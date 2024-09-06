from .base import *
import os
import dj_database_url
env = os.environ.copy()

DATABASES['default'] = dj_database_url.config(
    default=env['DATABASE_URL'],
    conn_max_age=600,
    conn_health_checks=True,
)



SECRET_KEY = env["SECRET_KEY"]
ALLOWED_HOSTS = ["*"]

DEBUG = False

try:
    from .local import *
except ImportError:
    pass
