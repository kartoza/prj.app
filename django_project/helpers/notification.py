from pinax.notifications.models import send


def send_notification(*args, **kwargs):
    """
    Interface for pinax send function.
    """
    if 'request_user' in kwargs:
        kwargs['extra_context']['request_user'] = kwargs['request_user']
        del kwargs['request_user']
    return send(*args, **kwargs)
