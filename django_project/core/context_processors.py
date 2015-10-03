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
