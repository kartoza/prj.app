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
    'django_countries',  # for sponsor addresses
    # 'user_map',
    'disqus',
)

# Set disqus and shortname
# noinspection PyUnresolvedReferences
from .secret import DISQUS_WEBSITE_SHORTNAME  # noqa

MIGRATION_MODULES = {'accounts': 'core.migration'}

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

# Contributed / third party js and css libs for pipeline compression
# For hand rolled js and css for this app, use project.py
PIPELINE = {
    'JAVASCRIPT': {},
    'STYLESHEETS': {},
}

# These get enabled in prod.py
PIPELINE_ENABLED = False
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

# Add PipelineFinder to STATICFILES_FINDERS
STATICFILES_FINDERS += (
    'pipeline.finders.PipelineFinder',
)

# Django-allauth related settings

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

INSTALLED_APPS += (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
)

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FORM_CLASS = 'base.forms.SignupForm'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
