from django.test import TestCase, Client
from django.test.utils import override_settings
from django.urls import reverse
from django.contrib.sessions.backends.db import SessionStore

from base.tests.model_factories import ProjectF
from certification.tests.model_factories import StatusF
from core.model_factories import UserF


class TestGetStatus(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        self.project = ProjectF.create()
        self.status = StatusF.create(
            project=self.project
        )
        self.api_url = reverse('get-status-list', kwargs={
            'project_slug': self.project.slug
        }).replace(
            'en-us', 'en'
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_get_status_no_login(self):
        response = self.client.get(
            self.api_url
        )
        self.assertEqual(
            response.status_code,
            302
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_get_status_login(self):
        user = UserF.create(**{
            'username': 'admin',
            'password': 'password',
            'email': 'test@test.com',
            'is_staff': True
        })
        user.set_password('password')
        user.save()
        self.client.login(
            username='admin',
            password='password'
        )
        response = self.client.get(self.api_url)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(
            response.json()[0]['id'],
            self.status.id
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_get_status_no_project(self):
        user = UserF.create(**{
            'username': 'admin',
            'password': 'password',
            'email': 'test@test.com',
            'is_staff': True
        })
        user.set_password('password')
        user.save()
        self.client.login(
            username='admin',
            password='password'
        )
        response = self.client.get(
            self.api_url.replace(self.project.slug, 'error'))
        self.assertTrue(response.status_code, 400)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_get_status_with_session(self):
        session = SessionStore()
        session.create()

        self.api_url += f'?s={session.session_key}'

        response = self.client.get(
            self.api_url
        )
        self.assertTrue(response.status_code, 200)
        self.assertEqual(
            response.json()[0]['id'],
            self.status.id
        )
