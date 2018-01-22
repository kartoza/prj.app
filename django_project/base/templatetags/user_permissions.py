from django import template

register = template.Library()


@register.filter(name='has_permission', is_safe=True)
def has_permission(user, permission_name):
    permission = user.user_permissions.get(codename=permission_name)
    if permission in user.user_permissions.all():
        return True
    else:
        return False
