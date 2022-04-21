from django.test import TestCase, Client
from django.test.utils import override_settings
from django.urls import reverse
from base.models import Project
from base.tests.model_factories import ProjectF
from core.model_factories import UserF


class TestExternalReviewer(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        self.user = UserF.create(**{
            'username': 'admin',
            'password': 'password',
            'email': 'test@test.com',
            'is_staff': True
        })
        self.user.set_password('password')
        self.user.save()
        self.client.login(
            username='admin',
            password='password'
        )
        self.project = ProjectF.create(
            owner=self.user
        )
        self.api_url = reverse('update-external-reviewer-text', kwargs={
            'project_slug': self.project.slug
        }).replace('en-us', 'en')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_external_reviewer_text(self):
        data = {
            'text': ''
        }
        self.client.login(
            username='admin',
            password='password'
        )
        response = self.client.post(
            self.api_url,
            data
        )
        self.assertTrue(response.status_code, 404)
        data = {
            'text': 'test'
        }
        response = self.client.post(
            self.api_url,
            data
        )
        self.assertTrue(response.status_code, 302)
        project = Project.objects.get(id=self.project.id)
        self.assertEqual(
            project.external_reviewer_invitation,
            'test'
        )
