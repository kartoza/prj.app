# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/02/18'

from rolepermissions.roles import AbstractUserRole


class DataAdmin(AbstractUserRole):
    available_permissions = {
        'can_create_data': True,
        'can_update_data': True,
        'can_delete_data': True,
    }


class User(AbstractUserRole):
    available_permissions = {}


class Validator(AbstractUserRole):
    available_permissions = {
        'can_validate_data': True
    }
