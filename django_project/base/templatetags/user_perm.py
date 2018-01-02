from django import template
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter(name='has_perm')
def has_perm(user, perm_name):
    perm = get_object_or_404(Permission, name=perm_name)
    # perm = Permission.objects.get(name=perm_name)
    perms = perm.permissions.all()
    if perms:
        return perm in user.get_all_permissions()
    else:
        return ""
