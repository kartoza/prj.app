
"""Configuration for production server."""
# noinspection PyUnresolvedReferences
from .prod import *  # noqa
import os
import ast
print(os.environ)

DEBUG = False

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Dimas Ciputra', 'dimas@kartoza.com'),
    ('Sumandari', 'sumandari@kartoza.com'),)

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
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND',
                               'gmailapi_backend.mail.GmailBackend')
# Host for sending e-mail.
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp')
# Port for sending e-mail.
EMAIL_PORT = ast.literal_eval(os.environ.get('EMAIL_PORT', '25'))
# SMTP authentication information for EMAIL_HOST.
# See fig.yml for where these are defined
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'noreply@kartoza.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'docker')
EMAIL_USE_TLS = ast.literal_eval(os.environ.get('EMAIL_USE_TLS', 'False'))
EMAIL_USE_SSL = ast.literal_eval(os.environ.get('EMAIL_USE_SSL', 'False'))
EMAIL_SUBJECT_PREFIX = os.environ.get('EMAIL_SUBJECT_PREFIX', '[PROJECTA]')
