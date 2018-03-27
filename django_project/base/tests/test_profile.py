# coding=utf-8
"""Tests for models."""

from django.test import TestCase
from base.tests.model_factories import ProfileF
from core.tests.model_factories import UserF


class TestProfile(TestCase):
    """ Tests CURD Profile.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_profile_create(self):
        """
        Tests profile creation
        """
        user = UserF.create()
        ProfileF.create(user=user)

        # check if pk exists
        self.assertTrue(user.profile.pk is not None)

        # check if qualifications and other exists
        self.assertTrue(user.profile.qualifications is not None)
        self.assertTrue(user.profile.other is not None)

    def test_profile_read(self):
        """
        Tests profile creation
        """
        user = UserF.create()
        ProfileF.create(
            user=user,
            qualifications='qualifications',
            other='other'
        )
        user.profile.save()

        self.assertTrue(user.profile.qualifications == 'qualifications')
        self.assertTrue(
            user.profile.other == 'other')

    def test_profile_update(self):
        """
        Tests profile creation
        """
        user = UserF.create()
        ProfileF.create(
            user=user
        )
        profile_data = {
            'qualifications': 'qualifications',
            'other': 'other'
        }
        user.profile.__dict__.update(profile_data)
        user.profile.save()

        # check if updated
        for key, val in profile_data.items():
            self.assertEqual(getattr(user.profile, key), val)

    def test_profile_delete(self):
        """
        Tests fish collection record model delete
        """
        user = UserF.create()
        profile = ProfileF.create(
            user=user
        )
        profile.delete()

        # check if deleted
        self.assertTrue(user.profile.pk is None)
