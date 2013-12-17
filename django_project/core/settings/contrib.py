from .base import *

# Extra installed apps
INSTALLED_APPS += (
    # 'raven.contrib.django',  # enable Raven plugin
    'south',
    'crispy_forms',
    'pipeline',
    'widget_tweaks',  # lets us add some bootstrap css to form elements
    'accounts',  # userena
    'guardian',  # for userena
    'easy_thumbnails',  # also needed for userena
    'userena',
    'raven.contrib.django',
    'reversion',
)

DEFAULT_FILE_STORAGE = ('django_hashedfilenamestorage.storage'
                        '.HashedFilenameFileSystemStorage')

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# use underscore template function
PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

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
