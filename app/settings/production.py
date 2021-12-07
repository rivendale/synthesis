from .base import *  # noqa # pylint: disable=unused-wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*', '127.0.0.1', '0.0.0.0', 'synthesis.page',
                 os.getenv('ALLOWED_LOCAL_HOST', '')]
