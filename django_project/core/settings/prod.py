# coding=utf-8

"""Project level settings."""
from .project import *  # noqa

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# Localhost:9000 for vagrant
# Changes for live site
# ['*'] for testing but not for production

ALLOWED_HOSTS = [
    'localhost:9000',
]

INSTALLED_APPS += (
    'pipeline',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS += (
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'PIPELINE_ENABLED': True,
}

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SERVER_EMAIL = 'dimas@kartoza.com'
EMAIL_HOST = 'kartoza.com'
DEFAULT_FROM_EMAIL = 'dimas@kartoza.com'
