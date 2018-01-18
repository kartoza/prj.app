from django import template

register = template.Library()


@register.filter(name='has_perm', is_safe=True)
def has_perm(user, perm_name):
    perm = user.user_permissions.get(codename=perm_name)
    if perm in user.user_permissions.all():
     return True
    else:
        return False

