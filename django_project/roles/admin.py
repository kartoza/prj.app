# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/02/18'

import json

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group, User
from django.contrib.gis import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from base.models.profile import Profile
from rolepermissions.admin import RolePermissionsUserAdminMixin
from rolepermissions.roles import RolesManager

admin.site.unregister(User)
admin.site.unregister(Group)


class ProfileInline(admin.StackedInline):
    model = Profile
    classes = ('collapse open',)
    inline_classes = ('collapse open',)


class RolePermissionsUserForm(UserChangeForm):
    class Media:
        css = {
            'all': ('/static/css/role-admin-form.css',)
        }
        js = (
            '/static/libs/jquery/jquery-3.3.1.min.js',
            '/static/js/role-admin-form.js')


class RolePermissionsUserAdmin(RolePermissionsUserAdminMixin, UserAdmin):
    """ Displaying user using rolepermission library.
    Hide permissions because it will be
    automatically assign if groups is changed.
    """
    inlines = (ProfileInline,)
    form = RolePermissionsUserForm
    list_display = (
        'username', 'email',
        'first_name', 'last_name', 'is_staff',
        'roles', 'date_joined', 'last_login')
    list_filter = ('date_joined', 'last_login', 'is_staff')
    readonly_fields = ('role_permissions', 'all_roles_permissions')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email')}),
        (_('Roles'), {'fields': (
            'groups', 'role_permissions', 'all_roles_permissions')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser'
        )})
    )

    def roles(self, obj):
        roles = []
        for group in obj.groups.all():
            roles.append(group.name)
        return ','.join(roles)

    def role_permissions(self, obj):
        permissions = []
        for permission in obj.user_permissions.all():
            permissions.append(
                '- %s' % permission.name.replace('auth | user | ', '')
            )
        if permissions:
            return format_html('<br>'.join(permissions))
        else:
            return '-'

    def all_roles_permissions(self, obj):
        # get all roles permission in json structure
        roles_json = {}
        for role in RolesManager.get_roles():
            roles_json[role.get_name()] = [
                '- %s' % permission
                for permission in list(role.permission_names_list())
            ]
        return json.dumps(roles_json)

    role_permissions.allow_tags = True


admin.site.register(User, RolePermissionsUserAdmin)
