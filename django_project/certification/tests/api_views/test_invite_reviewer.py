from django.core import mail
from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse

from core.model_factories import UserF
from certification.tests.model_factories import (
    ProjectF, CertifyingOrganisationF
)


class TestInviteReviewer(TestCase):
    """Test invite reviewer."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """Set up before each test."""
        self.client = Client()
        self.client.post(
                '/set_language/', data={'language': 'en'})
        self.project_owner = UserF.create(**{
            'username': 'test',
            'password': 'password',
            'is_staff': False
        })
        self.project_owner.set_password('password')
        self.project_owner.save()
        self.project = ProjectF.create(
            owner=self.project_owner
        )
        self.superuser = UserF.create(**{
            'username': 'super',
            'password': 'password',
            'is_staff': True,
            'is_superuser': True
        })
        self.superuser.set_password('password')
        self.superuser.save()
        self.user_manager = UserF.create(**{
            'username': 'manager',
            'password': 'password',
            'is_staff': True,
            'is_superuser': True
        })
        self.user_manager.set_password('password')
        self.user_manager.save()
        self.project.certification_managers.add(self.user_manager)
        self.certifying_organisation = CertifyingOrganisationF.create(
            project=self.project
        )
        self.url = reverse('invite-external-reviewer', kwargs={
            'project_slug': self.project.slug,
            'slug': self.certifying_organisation.slug
        })
        self.url = self.url.replace('us-en', 'en')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_invite_reviewer_no_login(self):
        data = {
            'email': 'test@gmail.com'
        }
        response = self.client.post(self.url, data)
        self.assertTrue(response.status_code, 400)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_invite_reviewer_invalid_organisation(self):
        url = self.url.replace(
            self.certifying_organisation.slug,
            'no-org'
        )
        response = self.client.post(
            url, {}
        )
        self.assertTrue(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_invite_reviewer_invalid_email(self):
        data = {
            'email': 'error'
        }
        self.client.login(
            username=self.superuser.username,
            password='password'
        )
        response = self.client.post(self.url, data)
        self.assertTrue(response.status_code, 404)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_invite_reviewer_access(self):
        data = {
            'email': 'test@gmail.com'
        }

        # Admin/staff user
        self.client.login(
            username=self.superuser.username,
            password='password'
        )
        response = self.client.post(self.url, data)
        self.assertTrue(response.status_code, 200)
        json_response = response.json()
        self.assertTrue(
            json_response['created']
        )
        self.assertIn(
            'You have been invited as a reviewer',
            mail.outbox[0].subject)
        self.assertEqual(
            data['email'],
            mail.outbox[0].to[0])

        # Project owner
        self.client.login(
            username=self.project_owner.username,
            password='password'
        )
        response = self.client.post(self.url, data)
        self.assertTrue(response.status_code, 200)
        json_response = response.json()
        self.assertFalse(
            json_response['created']
        )

        # Certification manager
        self.client.login(
            username=self.user_manager.username,
            password='password'
        )
        response = self.client.post(self.url, data)
        self.assertTrue(response.status_code, 200)
        json_response = response.json()
        self.assertFalse(
            json_response['created']
        )
