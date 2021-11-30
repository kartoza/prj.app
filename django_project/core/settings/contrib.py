# coding=utf-8
"""
core.settings.contrib
"""
from .base import *  # noqa

# Extra installed apps - grapelli needs to be added before others
INSTALLED_APPS = [
    'grappelli',
] + INSTALLED_APPS

INSTALLED_APPS += [
    'modeltranslation',
    'raven.contrib.django.raven_compat',  # enable Raven plugin
    'crispy_forms',
    'widget_tweaks',  # lets us add some bootstrap css to form elements
    'easy_thumbnails',
    'reversion',
    'rosetta',
    'embed_video',
    'django_hashedfilenamestorage',
    'django_countries',  # for sponsor addresses
    'colorfield',  # for color picker
    # 'user_map',
    # 'disqus',  # disabled because of unwanted ads.
    'rest_framework',
    'simple_history',
    'djstripe',
    'preferences',
    'pinax.notifications',
    'tinymce',  # rich text editor
]

# Add preferences to context_processors
TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'preferences.context_processors.preferences_cp'
)

# Set disqus and shortname
# noinspection PyUnresolvedReferences
from .secret import DISQUS_WEBSITE_SHORTNAME  # noqa

MIGRATION_MODULES = {'accounts': 'core.migration'}

GRAPPELLI_ADMIN_TITLE = 'Site administration panel'

STOP_WORDS = (
    'a', 'an', 'and', 'if', 'is', 'the', 'in', 'i', 'you', 'other',
    'this', 'that', 'to',
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

INSTALLED_APPS += [
    'pipeline',
]

MIDDLEWARE += [
    # For rosetta localisation
    'django.middleware.locale.LocaleMiddleware',
]

DEFAULT_FILE_STORAGE = (
    'django_hashedfilenamestorage.storage.HashedFilenameFileSystemStorage')

# use underscore template function
PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Contributed / third party js libs for pipeline compression
# For hand rolled js for this app, use project.py
PIPELINE = {
    'PIPELINE_ENABLED': False,
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
    'JAVASCRIPT': {
        'contrib': {
            'source_filenames': (
                'js/gifffer.js',
            ),
            'output_filename': 'js/contrib.js',
        }
    },
    'STYLESHEETS': {
    }
}

# Django-allauth related settings

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

INSTALLED_APPS += [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': ['user:email', 'read:org']
    }
}

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FORM_CLASS = 'base.forms.SignupForm'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

# Stripe keys
STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "")
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "sk_live_")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_")
STRIPE_LIVE_MODE = False  # Change to True in production
# Get it from the section in the Stripe dashboard where you added the
# webhook endpoint
DJSTRIPE_WEBHOOK_SECRET = os.environ.get('DJSTRIPE_WEBHOOK_SECRET', 'whsec_x')

INSTALLED_APPS += [
    'gmailapi_backend',
]
# django-gmailapi-backend
GMAIL_API_CLIENT_ID = os.environ.get('GMAIL_API_CLIENT_ID', '')
GMAIL_API_CLIENT_SECRET = os.environ.get('GMAIL_API_CLIENT_SECRET', '')
GMAIL_API_REFRESH_TOKEN = os.environ.get('GMAIL_API_REFRESH_TOKEN', '')
