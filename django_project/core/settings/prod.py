# coding=utf-8

"""Project level settings."""
from os.path import join, dirname, exists
from .project import *  # noqa

try:
    from .secret import SENTRY_KEY
except ImportError:
    SENTRY_KEY = None


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# Localhost:9000 for vagrant
# Changes for live site
# ['*'] for testing but not for production

ALLOWED_HOSTS = [
    'localhost:9000',
    'geocontext.kartoza.com'
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

# Logging
if 'raven.contrib.django.raven_compat' in INSTALLED_APPS and SENTRY_KEY:
    # noinspection PyUnresolvedReferences
    import raven  # noqa

    version_file = join(dirname(dirname(dirname(__file__))), '.version')
    if exists(version_file):
        with open(version_file, 'r') as version:
            release = version.read()
    else:
        release = 'unknown'

    RAVEN_CONFIG = {
        # Self hosted sentry
        'dsn': SENTRY_KEY,
        'release': release,
    }

    MIDDLEWARE = (
        # We recommend putting this as high in the chain as possible
        # see http://raven.readthedocs.org/en/latest/integrations/  ...
        # ... django.html#message-references
        # This will add a client unique id in messages
        'raven.contrib.django.raven_compat.middleware.'
        'SentryResponseErrorIdMiddleware',
    ) + MIDDLEWARE

    # Sentry settings - logs exceptions to a database
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class':
                    'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'null': {
                'class': 'django.utils.log.NullHandler',
            },
        },
        'loggers': {
            # Special rules to not bother logging when host is
            # not allowed otherwise we get lots of mail spam....
            'django.security.DisallowedHost': {
                'handlers': ['null'],
                'propagate': False,
            },
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }
