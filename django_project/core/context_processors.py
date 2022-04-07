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


def sustaining_member_context(request):
    """Context processor for sustaining member data.
    :param request: Http request object
    :returns: A dict containing the following:
        * is_sustaining_member: Whether user is a sustaining member or not
    :rtype: dict
    """
    from changes.models import active_sustaining_membership
    from base.models import Project

    context_data = {
        'is_sustaining_member': False
    }
    user = request.user
    project = None
    if not user or user.is_anonymous:
        return context_data
    if hasattr(request, 'resolver_match'):
        try:
            project_slug = request.resolver_match.kwargs.get('project_slug')
            if not project_slug:
                project_slug = request.resolver_match.kwargs.get('slug')
            try:
                project = Project.objects.get(
                    slug=project_slug
                )
            except Project.DoesNotExist:
                return context_data
        except AttributeError:
            return context_data
    context_data['is_sustaining_member'] = active_sustaining_membership(
                user,
                project
            ).exists()
    return context_data
