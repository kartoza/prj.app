from django import template
from django.contrib.auth.models import User


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_user_perm(context, perm):
    try:
        request = context['request']
        # obj = Project.objects.get(user=request.user)
        obj = User.objects.get(user=request.user)
        obj_perms = obj.permission_tags.all()
        flag = False
        for p in obj_perms:
            if perm.lower() == p.codename.lower():
                flag = True
                return flag
        return flag
    except:
        return ""
