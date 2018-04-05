
"""Configuration for production server."""
# noinspection PyUnresolvedReferences
from .prod import *  # noqa
import os
print os.environ

DEBUG = False

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Tim Sutton', 'tim@kartoza.com'),
    ('Christian Christellis', 'christian@kartoza.com'),
    ('Anita Hapsari', 'anita@kartoza.com'),)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USERNAME'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': 5432,
        'TEST': {
            'NAME': 'unittests',
        }
    }
}


# See fig.yml file for postfix container definition
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
EMAIL_HOST = 'smtp'
# Port for sending e-mail.
EMAIL_PORT = 25
# SMTP authentication information for EMAIL_HOST.
# See fig.yml for where these are defined
EMAIL_HOST_USER = 'noreply@kartoza.com'
EMAIL_HOST_PASSWORD = 'docker'
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = '[PROJECTA]'
