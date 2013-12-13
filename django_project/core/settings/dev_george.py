__author__ = 'georgeirwin'

from .project import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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
        #     'visual_changelog.db')),
        'NAME': 'changelog',
        # The following settings are not used with sqlite3:
        'USER': 'wsgi',
        'PASSWORD': 'vagrant',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}
