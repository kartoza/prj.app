# coding=utf-8

import json

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
        self.user = UserF.create(**{
            'username': 'anita',
            'password': 'password',
            'is_staff': True
        })
        self.user.set_password('password')
        self.user.save()
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
            project=self.project,
            approved=True)

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
        items = json.loads(response._container[1])['rss']['channel']['item']
        self.assertGreater(
            len(items), 0, 'There should be non empty list of sponsor')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_is_JSON_feed(self):
        response = self.client.get(reverse('sponsor-json-feed', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(
            'application/json; charset=utf-8',
            response._headers['content-type'][1])
