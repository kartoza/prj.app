# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/02/18'

from rolepermissions.roles import AbstractUserRole


class Role1(AbstractUserRole):
    role_name = 'role_1'
    available_permissions = {
        'permission_1': True,
        'permission_2': True
    }


class Role2(AbstractUserRole):
    role_name = 'role_2'
    available_permissions = {
        'permission_1': True,
        'permission_3': True,
    }
