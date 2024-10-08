from .base import *
import os
import dj_database_url
env = os.environ.copy()

INSTALLED_APPS += [
    'storages',
]

DATABASES['default'] = dj_database_url.config(
    default=env['DATABASE_URL'],
    conn_max_age=600,
    conn_health_checks=True,
)



SECRET_KEY = env["SECRET_KEY"]
ALLOWED_HOSTS = ["*"]

AWS_ACCESS_KEY_ID = env["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = env["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = 'sanscodex'
AWS_S3_REGION_NAME = 'eu-central-1'  # Örneğin 'eu-central-1'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = False

MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{AWS_S3_REGION_NAME}/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEBUG = True

try:
    from .local import *
except ImportError:
    pass
