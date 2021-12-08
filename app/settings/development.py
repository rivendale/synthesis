from .base import *  # noqa # pylint: disable=unused-wildcard-import


DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1', '0.0.0.0', 'localhost',
                 os.getenv('ALLOWED_LOCAL_HOST', '')]

CORS_ORIGIN_WHITELIST = []

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
