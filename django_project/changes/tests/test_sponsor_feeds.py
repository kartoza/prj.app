# coding=utf-8
"""Test for RSS and JSON feed for Sponsor and Past Sponsor"""
import datetime
import urllib
import logging

from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.test.client import Client
from base.tests.model_factories import ProjectF
from changes.tests.model_factories import (
    SponsorshipLevelF,
    SponsorF,
    SponsorshipPeriodF)
from core.model_factories import UserF


class TestSponsorFeeds(TestCase):
    """Test for sponsor feed in RSS and JSON."""

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

        self.sponsorship_level = SponsorshipLevelF.create(
            project=self.project,
            name='Gold')

        # Current sponsor
        self.current_sponsor = SponsorF.create(
            project=self.project,
            name='Current Sponsor')
        self.current_sponsorship_period = SponsorshipPeriodF.create(
            sponsor=self.current_sponsor,
            sponsorship_level=self.sponsorship_level,
            project=self.project,
            approved=True,
            start_date=datetime.datetime.now() - datetime.timedelta(days=180),
            end_date=datetime.datetime.now() + datetime.timedelta(days=365),
        )

        # Past sponsor under a certain time limit, in this case 1 year
        self.past_sponsor = SponsorF.create(
            project=self.project,
            name='Past Sponsor')
        self.past_sponsorship_period = SponsorshipPeriodF.create(
            sponsor=self.past_sponsor,
            sponsorship_level=self.sponsorship_level,
            project=self.project,
            approved=True,
            start_date=datetime.datetime.now() - datetime.timedelta(days=180),
            end_date=datetime.datetime.now() - datetime.timedelta(days=30)
        )

        # It's a very old sponsor that will not be shown
        self.one_decade_ago_sponsor = SponsorF.create(
            project=self.project,
            name='One Decade Ago Sponsor')
        self.one_decade_ago_sponsorship_period = SponsorshipPeriodF.create(
            sponsor=self.one_decade_ago_sponsor,
            sponsorship_level=self.sponsorship_level,
            project=self.project,
            approved=True,
            start_date=datetime.datetime.now() - datetime.timedelta(days=4000),
            end_date=datetime.datetime.now() - datetime.timedelta(days=3650)
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        self.project.delete()
        self.current_sponsor.delete()
        self.sponsorship_level.delete()
        self.current_sponsorship_period.delete()
        self.past_sponsor.delete()
        self.past_sponsorship_period.delete()
        self.one_decade_ago_sponsor.delete()
        self.one_decade_ago_sponsorship_period.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_current_sponsor_rss_feed_view(self):
        response = self.client.get(reverse('sponsor-rss-feed', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, True)
        self.assertEqual(self.past_sponsor.name in response.content, False)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, False)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_past_sponsor_rss_feed_view_without_years_limit(self):
        response = self.client.get(reverse('past-sponsor-rss-feed', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, False)
        self.assertEqual(self.past_sponsor.name in response.content, True)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, True)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_past_sponsor_rss_feed_view_with_years_limit(self):
        url_with_limit = reverse('past-sponsor-rss-feed', kwargs={
            'project_slug': self.project.slug
        })
        url_with_limit += '?' + urllib.urlencode({'years_limit': 2})
        response = self.client.get(url_with_limit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, False)
        self.assertEqual(self.past_sponsor.name in response.content, True)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, False)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_past_sponsor_rss_feed_view_with_invalid_years_limit(self):
        """test_past_sponsor_rss_feed_view_with_invalid_years_limit

        It will return all past sponsors.
        """
        url_with_limit = reverse('past-sponsor-rss-feed', kwargs={
            'project_slug': self.project.slug
        })
        url_with_limit += '?' + urllib.urlencode({'years_limit': 'a'})
        response = self.client.get(url_with_limit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, False)
        self.assertEqual(self.past_sponsor.name in response.content, True)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, True)

        url_with_limit = reverse('past-sponsor-rss-feed', kwargs={
            'project_slug': self.project.slug
        })
        url_with_limit += '?' + urllib.urlencode({'years_limit': -1})
        response = self.client.get(url_with_limit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, False)
        self.assertEqual(self.past_sponsor.name in response.content, True)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, True)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_current_sponsor_json_feed_view(self):
        response = self.client.get(reverse('sponsor-json-feed', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, True)
        self.assertEqual(self.past_sponsor.name in response.content, False)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, False)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_past_sponsor_json_feed_view_without_years_limit(self):
        response = self.client.get(reverse('past-sponsor-json-feed', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, False)
        self.assertEqual(self.past_sponsor.name in response.content, True)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, True)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_past_sponsor_json_feed_view_with_years_limit(self):
        url_with_limit = reverse('past-sponsor-json-feed', kwargs={
            'project_slug': self.project.slug
        })
        url_with_limit += '?' + urllib.urlencode({'years_limit': 2})
        response = self.client.get(url_with_limit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, False)
        self.assertEqual(self.past_sponsor.name in response.content, True)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, False)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_past_sponsor_json_feed_view_with_invalid_years_limit(self):
        """test_past_sponsor_json_feed_view_with_invalid_years_limit

        It will return all past sponsors.
        """
        url_with_limit = reverse('past-sponsor-json-feed', kwargs={
            'project_slug': self.project.slug
        })
        url_with_limit += '?' + urllib.urlencode({'years_limit': 'a'})
        response = self.client.get(url_with_limit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, False)
        self.assertEqual(self.past_sponsor.name in response.content, True)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, True)

        url_with_limit = reverse('past-sponsor-json-feed', kwargs={
            'project_slug': self.project.slug
        })
        url_with_limit += '?' + urllib.urlencode({'years_limit': -1})
        response = self.client.get(url_with_limit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.current_sponsor.name in response.content, False)
        self.assertEqual(self.past_sponsor.name in response.content, True)
        self.assertEqual(
            self.one_decade_ago_sponsor.name in response.content, True)
