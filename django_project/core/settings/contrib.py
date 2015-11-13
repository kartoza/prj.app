# coding=utf-8
"""
core.settings.contrib
"""
from .base import *  # noqa

# Extra installed apps
INSTALLED_APPS = (
    'grappelli',
) + INSTALLED_APPS

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',  # enable Raven plugin
    'crispy_forms',
    'widget_tweaks',  # lets us add some bootstrap css to form elements
    'accounts',  # userena
    'guardian',  # for userena
    'easy_thumbnails',  # also needed for userena
    'userena',
    'reversion',
    'rosetta',
    'embed_video',
    # 'user_map',
)

STOP_WORDS = (
    'a', 'an', 'and', 'if', 'is', 'the', 'in', 'i', 'you', 'other',
    'this', 'that'
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Added for userena
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.Profile'
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

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
    # for django-audited-models
    # Threaded middleware *must* come *after* auth middleware
    'threaded_multihost.middleware.ThreadLocalMiddleware',
    # For rosetta localisation
    'django.middleware.locale.LocaleMiddleware'
)

DEFAULT_FILE_STORAGE = (
    'django_hashedfilenamestorage.storage.HashedFilenameFileSystemStorage')

# use underscore template function
PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Contributed / third party js libs for pipeline compression
# For hand rolled js for this app, use project.py
PIPELINE_JS = {
    # 'contrib': {
    #     'source_filenames': (
    #         'js/jquery-1.11.3.js',
    #         'js/underscore.1.8.3.js',
    #         'js/bootstrap-3.3.5.js'
    #     ),
    #     'output_filename': 'js/contrib.js',
    # }
}

# Contributed / third party css for pipeline compression
# For hand rolled css for this app, use project.py
PIPELINE_CSS = {
    # 'contrib': {
    #     'source_filenames': (
    #         'css/bootstrap.3.3.5.css',
    #         'css/bootstrap-theme.3.3.5.css',
    #     ),
    #     'output_filename': 'css/contrib.css',
    #     'extra_context': {
    #         'media': 'screen, projection',
    #     },
    # }
}

# These get enabled in prod.py
PIPELINE_ENABLED = False
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
