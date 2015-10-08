# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os  # noqa
from .contrib import *  # noqa

# Project apps
INSTALLED_APPS += (
    'base',
    'changes',
    'github_issue',
    'vota',
    'disqus',
)

# How many versions to list in each project box
PROJECT_VERSION_LIST_SIZE = 10

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False
