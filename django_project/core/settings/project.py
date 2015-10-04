# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""
import os  # noqa
from .contrib import *  # noqa

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'ENGINE': 'django.db.backends.sqlite3',
        #Or path to database file if using sqlite3.
        # 'NAME': os.path.abspath(os.path.join(
        #     os.path.dirname(__file__),
        #     os.path.pardir,
        #     os.path.pardir,
        #     os.path.pardir,
        #     'resources',
        #     'sqlite',
        #     'projecta.db')),
        'NAME': 'changelog',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

# Project apps
INSTALLED_APPS += (
    'base',
    'changes',
    'github_issue',
    'vota',
    'disqus',
)

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False

PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/jquery-1.10.1.min.js',
            'js/csrf-ajax.js',
            'js/underscore-min.js',
            'js/bootstrap.min.js',
            'js/changelog.js',
            'js/github-issue.js',
        ),
        'output_filename': 'js/contrib.js',
    }
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/bootstrap.min.css',
            'css/bootstrap-theme.min.css',
            'css/changelog.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    }
}

PIPELINE_JS_COMPRESSOR = None

