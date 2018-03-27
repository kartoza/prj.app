# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/02/18'

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rolepermissions.roles import remove_role

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """ Unassign role to user.
    """
    args = '<message>'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('role')

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']
        if username and role:
            try:
                user = User.objects.get(username=username)
                remove_role(user, role)
                print('success')
            except User.DoesNotExist:
                print('user does not found')
