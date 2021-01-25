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
INSTALLED_APPS += [
    'base',
    'changes',
    'github_issue',
    'vota',
    'certification',
    'lesson',
]

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


MIDDLEWARE += [
    # For nav bar generation
    'core.custom_middleware.NavContextMiddleware',
]

# Project specific javascript files to be pipelined
# For third party libs like jquery should go in contrib.py
PIPELINE['JAVASCRIPT']['project'] = {
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
PIPELINE['STYLESHEETS']['project'] = {
    'source_filenames': (
        'css/changelog.css',
        'css/form.css',
        'css/fonts.css',
        'css/base.css',
    ),
    'output_filename': 'css/project.css',
    'extra_context': {
        'media': 'screen,projection',
    },
}

VALID_DOMAIN = [
    'localhost',
    'changelog.kartoza.com',
    'staging.changelog.kartoza.com'
]

EMAIL_HOST_USER = 'noreply@kartoza.com'
LOGIN_URL = '/en/accounts/login/'

# The numeric mode (i.e. 0o644) to set newly uploaded files to.
FILE_UPLOAD_PERMISSIONS = 0o644
