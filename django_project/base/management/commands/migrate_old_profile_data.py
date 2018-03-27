# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/03/18'

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import ProgrammingError

from base.models.profile import Profile
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """ Assign role to user.
    """
    args = '<message>'
    profile_fields = [
        f.name
        for f in Profile._meta.get_fields()
        if (f.name != 'id' and f.name != 'user')
    ]
    user_fields = ['username',
                   'firstname', 'surname',
                   'email'] + profile_fields

    def get_old_users(self):
        cursor = connection.cursor()
        cursor.execute('SELECT %s FROM "User"' % ','.join(self.user_fields))
        row = cursor.fetchall()
        return row

    def handle(self, *args, **options):
        rows = []

        try:
            rows = self.get_old_users()
        except ProgrammingError:
            print("No old user data found")

        for row in rows:
            row_dictionary = {}

            for i, item in enumerate(self.user_fields):
                key = item
                row_dictionary[key] = row[i]

            # save to user
            user, created = User.objects.get_or_create(
                username=row_dictionary['username']
            )
            if created:
                user.first_name = row_dictionary['firstname']
                user.last_name = row_dictionary['surname']

                if row_dictionary['email']:
                    user.email = row_dictionary['email']
                user.save()

                print('%s : created' % user.username)

                # insert profile
                Profile.objects.create(user=user)
                profile = user.profile
                for field in self.profile_fields:
                    # TODO:
                    # If there are other type than char,
                    # please update to parse vale
                    value = row_dictionary[field]
                    if value:
                        setattr(profile, field, value)
                profile.save()
