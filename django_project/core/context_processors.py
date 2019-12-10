# coding=utf-8
"""
Our custom context processors
"""


# noinspection PyPep8Naming
def add_intercom_app_id(request):
    """Add our Intercom.io app ID to the context

    :param request: Http Request obj

    """
    try:
        from core.settings.private import INTERCOM_APP_ID
    except ImportError:
        INTERCOM_APP_ID = None

    if INTERCOM_APP_ID:
        return {'intercom_app_id': INTERCOM_APP_ID}
    else:
        return {}


def stripe_public_key(request):
    """Return stripe public key.
    :param request: Http Request obj
    """
    from django.conf import settings
    if settings.STRIPE_LIVE_MODE:
        return {'STRIPE_PUBLIC_KEY': settings.STRIPE_LIVE_PUBLIC_KEY}
    else:
        return {'STRIPE_PUBLIC_KEY': settings.STRIPE_TEST_PUBLIC_KEY}
