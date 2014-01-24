# coding=utf-8
"""
Our custom context processors
"""
from django.core.mail import mail_admins


def add_intercom_app_id(request):
    """Add our Intercom.io app ID to the context

    :param request: Http Request obj

    """
    from core.settings.private import INTERCOM_APP_ID

    if INTERCOM_APP_ID:
        return {'intercom_app_id': INTERCOM_APP_ID}
    else:
        mail_admins('No Intercom App ID!', 'Failed to find Intercom App ID')
        return {}