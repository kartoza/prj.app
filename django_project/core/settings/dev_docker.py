# -*- coding: utf-8 -*-
"""Settings for when running under docker in development mode."""
from .dev import *  # noqa

ALLOWED_HOSTS = ['*',
                 u'0.0.0.0']

ADMINS = ()

# Set debug to True for development
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}
