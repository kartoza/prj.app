# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.test.client import Client
from base.tests.model_factories import ProjectF
from changes.tests.model_factories import (
    SponsorshipLevelF,
    SponsorF,
    SponsorshipPeriodF)
from core.model_factories import UserF
import logging
import urllib2


class JSONFeedTest(TestCase):
    """JSON Feed unittest."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """
        Setup before each test

        We force the locale to en otherwise it will use
        the locale of the host running the tests and we
        will get unpredictable results / 404s
        """

        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.project = ProjectF.create(
            name='testproject')
        self.sponsor = SponsorF.create(
            project=self.project,
            name='Kartoza')
        self.sponsorship_level = SponsorshipLevelF.create(
            project=self.project,
            name='Gold')
        self.sponsorship_period = SponsorshipPeriodF.create(
            sponsor=self.sponsor,
            sponsorship_level=self.sponsorship_level,
            approved=True)
        self.user = UserF.create(**{
            'username': 'anita',
            'password': 'password',
            'is_staff': True
        })
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.sponsor.delete()
        self.sponsorship_level.delete()
        self.sponsorship_period.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_JSON_feed_view(self):
        response = self.client.get(reverse('sponsor-json-feed', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_is_JSON_feed(self):
        response = self.client.get(reverse('sponsor-json-feed', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(
            'application/json; charset=utf-8',
            response._headers['content-type'][1])
