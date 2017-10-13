
__author__ = 'rischan'

# -*- coding: utf-8 -*-
from .test import *  # noqa

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'test_db',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        # Set to empty string for default.
        'PORT': '',
    }
}

MEDIA_ROOT = '/tmp/media'
STATIC_ROOT = '/tmp/static'
