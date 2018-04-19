# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os  # noqa
from django.utils.translation import ugettext_lazy as _
from .utils import absolute_path
from .contrib import *  # noqa

# Project apps
INSTALLED_APPS += (
    'base',
    'changes',
    'github_issue',
    'vota',
    'certification',
    'lesson',
)

# Due to profile page does not available,
# this will redirect to home page after login
LOGIN_REDIRECT_URL = '/'

# How many versions to list in each project box
PROJECT_VERSION_LIST_SIZE = 10

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False


# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
    ('id', _('Indonesian')),
)

# Set storage path for the translation files
LOCALE_PATHS = (absolute_path('locale'),)


MIDDLEWARE_CLASSES = (
    # For nav bar generation
    'core.custom_middleware.NavContextMiddleware',
) + MIDDLEWARE_CLASSES

# Project specific javascript files to be pipelined
# For third party libs like jquery should go in contrib.py
PIPELINE_JS['project'] = {
    'source_filenames': (
        'js/csrf-ajax.js',
        'js/changelog.js',
        'js/github-issue.js',
        'js/entry.js',
        'js/category.js',
        'js/form.js',
    ),
    'output_filename': 'js/project.js',
}

# Project specific css files to be pipelined
# For third party libs like bootstrap should go in contrib.py
PIPELINE_CSS['project'] = {
    'source_filenames': (
        'css/changelog.css',
        'css/form.css',
        'css/fonts.css',
    ),
    'output_filename': 'css/project.css',
    'extra_context': {
        'media': 'screen, projection',
    },
}

VALID_DOMAIN = [
    'localhost',
    '0.0.0.0',
    'changelog.kartoza.com',
]
