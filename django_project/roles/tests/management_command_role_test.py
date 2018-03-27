# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/02/18'

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase


class ManagementCommandRoleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='username',
            password='password'
        )

    def test_management_command_assign_role(self):
        """ Tmanagement command assign role
        """
        call_command('sync_roles')

        permissions = self.user.user_permissions.all()
        permission_labels = [perm.name for perm in permissions]
        self.assertNotIn('Permission 1', permission_labels)
        self.assertNotIn('Permission 2', permission_labels)
        self.assertNotIn('Permission 3', permission_labels)

        call_command('assign_role', 'username', 'role_1')

        permissions = self.user.user_permissions.all()
        permission_labels = [perm.name for perm in permissions]
        self.assertIn('Permission 1', permission_labels)
        self.assertIn('Permission 2', permission_labels)
        self.assertNotIn('Permission 3', permission_labels)

        call_command('unassign_role', 'username', 'role_1')

        permissions = self.user.user_permissions.all()
        permission_labels = [perm.name for perm in permissions]
        self.assertNotIn('Permission 1', permission_labels)
        self.assertNotIn('Permission 2', permission_labels)
        self.assertNotIn('Permission 3', permission_labels)
