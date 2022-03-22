from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse

from core.model_factories import UserF
from .model_factories import ChecklistF, ProjectF, Checklist


class TestCertificationChecklist(TestCase):
    """Test certification checklist."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """Set up before each test."""
        self.client = Client()
        self.client.post(
                '/set_language/', data={'language': 'en'})
        self.project = ProjectF.create()
        self.user = UserF.create(**{
            'username': 'test',
            'password': 'password',
            'is_staff': False
        })
        self.user.set_password('password')
        self.user.save()
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
        self.checklist = ChecklistF.create(active=False, project=self.project)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.checklist.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_non_manager_activate_checklist(self):
        status = self.client.login(username='test', password='password')
        self.assertTrue(status)

        post_data = {
            'checklist_id': self.checklist.id
        }
        url = reverse('activate-checklist', kwargs={
            'project_slug': self.project.slug
        })

        response = self.client.post(url, post_data)
        self.assertEqual(
            response.status_code,
            403
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_manager_activate_checklist(self):
        post_data = {
            'checklist_id': self.checklist.id
        }
        # As manager
        self.client.login(username='manager', password='password')
        url = reverse('activate-checklist', kwargs={
            'project_slug': self.project.slug
        })

        response = self.client.post(url, post_data)
        self.assertEqual(
            response.status_code,
            200
        )
        checklist = Checklist.objects.get(id=self.checklist.id)
        self.assertTrue(checklist.active)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_manager_archive_checklist(self):
        post_data = {
            'checklist_id': self.checklist.id
        }
        # As manager
        self.client.login(username='manager', password='password')
        url = reverse('archive-checklist', kwargs={
            'project_slug': self.project.slug
        })

        response = self.client.post(url, post_data)
        self.assertEqual(
            response.status_code,
            200
        )
        checklist = Checklist.objects.get(id=self.checklist.id)
        self.assertFalse(checklist.active)
