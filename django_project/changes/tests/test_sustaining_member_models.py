# coding=utf-8
# flake8: noqa

from datetime import datetime
from django.test import TestCase, override_settings
from base.tests.model_factories import ProjectF
from changes.tests.model_factories import (
    SponsorF,
    SponsorshipPeriodF
)
from core.model_factories import UserF
from changes.models import active_sustaining_membership


class TestSustainingMemberModel(TestCase):
    """Tests sustaining member model."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """
        Setup before each test
        """
        self.user = UserF.create(**{
            'username': 'user',
            'password': 'password',
            'is_staff': False
        })
        self.user.set_password('password')
        self.user.save()
        self.project = ProjectF.create()
        self.sustaining_member = SponsorF.create(
            project=self.project,
            author=self.user
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SustainingMember_inactive(self):
        """
        Test if user is an inactive sustaining member
        """
        self.sustaining_member.sustaining_membership = True
        SponsorshipPeriodF.create(
            sponsor=self.sustaining_member,
            project=self.project,
            start_date=datetime(2014, 1, 1),
        )
        self.sustaining_member.active = False
        self.sustaining_member.save()
        self.assertFalse(
            active_sustaining_membership(self.user, self.project).exists())

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SustainingMember_active(self):
        """
        Test if user is an active sustaining member
        """
        self.sustaining_member.sustaining_membership = True
        SponsorshipPeriodF.create(
            sponsor=self.sustaining_member,
            project=self.project,
            start_date=datetime(2014, 1, 1),
        )

        self.sustaining_member.active = True
        self.sustaining_member.save()
        self.assertTrue(
            active_sustaining_membership(self.user, self.project).exists())
