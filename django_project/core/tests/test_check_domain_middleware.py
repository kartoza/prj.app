# coding=utf-8
import logging
from django.urls import reverse
from django.test import TestCase, override_settings
from django.test.client import Client


class TestCheckDomainMiddleware(TestCase):
    """Test that custom middleware to check domain works."""

    # Override settings to include django test default server in
    # valid domain list.
    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        logging.disable(logging.CRITICAL)

    # Override project settings to include testdomain as valid domain.
    @override_settings(VALID_DOMAIN=['testdomain', ])
    def test_valid_domain(self):
        client = Client(SERVER_NAME='testdomain')
        client.post(
            '/set_language/', data={'language': 'en'})
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'project/list.html', u'base/project_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    # Test checking domain on dev.
    @override_settings(DEBUG=True)
    def test_invalid_domain_dev(self):
        client = Client(SERVER_NAME='testdomain')
        client.post(
            '/set_language/', data={'language': 'en'})
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            expected_url='http://0.0.0.0:61202/en/domain-not-found/',
            fetch_redirect_response=False,
        )

    # Test checking domain on production.
    @override_settings(DEBUG=False)
    def test_invalid_domain_prod(self):
        client = Client(SERVER_NAME='testdomain')
        client.post(
            '/set_language/', data={'language': 'en'})
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            expected_url='http://changelog.kartoza.com/en/domain-not-found/',
            fetch_redirect_response=False,
        )
