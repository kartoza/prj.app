# coding=utf-8
"""
core.settings.contrib
"""
from .base import *  # noqa

# Extra installed apps - grapelli needs to be added before others
INSTALLED_APPS = (
    'grappelli',
) + INSTALLED_APPS

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',  # enable Raven plugin
    'crispy_forms',
    'widget_tweaks',  # lets us add some bootstrap css to form elements
    'easy_thumbnails',
    'reversion',
    'rosetta',
    'embed_video',
    'django_hashedfilenamestorage',
    # 'user_map',
)


MIGRATION_MODULES = {'accounts': 'core.null_migration'}

GRAPPELLI_ADMIN_TITLE = 'Site administration panel'

STOP_WORDS = (
    'a', 'an', 'and', 'if', 'is', 'the', 'in', 'i', 'you', 'other',
    'this', 'that'
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Easy-thumbnails options
THUMBNAIL_SUBDIR = 'thumbnails'
THUMBNAIL_ALIASES = {
    '': {
        'entry': {'size': (50, 50), 'crop': True},
        'medium-entry': {'size': (100, 100), 'crop': True},
        'large-entry': {'size': (400, 300), 'crop': True},
        'thumb300x200': {'size': (300, 200), 'crop': True},
    },
}

# Pipeline related settings

INSTALLED_APPS += (
    'pipeline',)

MIDDLEWARE_CLASSES += (
    # For rosetta localisation
    'django.middleware.locale.LocaleMiddleware',
)

DEFAULT_FILE_STORAGE = (
    'django_hashedfilenamestorage.storage.HashedFilenameFileSystemStorage')

# use underscore template function
PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Contributed / third party js libs for pipeline compression
# For hand rolled js for this app, use project.py
PIPELINE_JS = {}

# Contributed / third party css for pipeline compression
# For hand rolled css for this app, use project.py
PIPELINE_CSS = {}

# These get enabled in prod.py
PIPELINE_ENABLED = False
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
