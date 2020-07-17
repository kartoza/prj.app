# coding: utf-8
"""Unit tests for worksheet views."""

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__copyright__ = 'kartoza.com'


import logging

from django.test import TestCase, override_settings, Client
from django.urls import reverse

from lesson.tests.model_factories import WorksheetF
from lesson.tests.model_factories import SectionF
from base.tests.model_factories import ProjectF
from core.model_factories import UserF


class TestViews(TestCase):
    """Tests that Lesson Section views work."""

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def setUp(self):
        """
        Setup before each test
        We force the locale to en otherwise it will use
        the locale of the host running the tests and we
        will get unpredictable results / 404s
        """

        self.client = Client()
        self.client.post(
                '/set_language/', data = {'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.user = UserF.create(
            **{'username': 'sonlinux', 'is_staff': True})
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

        # Create project
        self.test_project = ProjectF.create()

        # Create section
        self.test_section = SectionF.create(project=self.test_project)
        self.test_worksheet = WorksheetF.create(section=self.test_section)
        self.kwargs_project = {'project_slug': self.test_section.project.slug}
        self.kwargs_section = {'slug': self.test_section.slug}
        self.kwargs_section_full = {
            'project_slug': self.test_section.project.slug,
            'slug': self.test_section.slug
        }
        self.kwargs_worksheet_full = {
            'project_slug': self.test_section.project.slug,
            'section_slug': self.test_section.slug,
            'pk': self.test_worksheet.pk
        }

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetCreateView(self):
        """Test accessing worksheet create view with no login."""

        post_data = {
            'module': u'Demo worksheet name',
            'title': u'Demo worksheet title',
            'section': self.test_section.id,
        }
        response = self.client.post(
                reverse('worksheet-create', kwargs = {
                    'project_slug': self.test_section.project.slug,
                    'section_slug': self.test_section.slug}),
                post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetCreateView_with_login(self):
        """Test accessing worksheet create view with login."""

        status = self.client.login(username='sonlinux', password='password')
        self.assertTrue(status)
        post_data = {
            'module': u'Demo worksheet name',
            'title': u'Demo worksheet title',
            'section': self.test_section.id,
        }
        response = self.client.post(
                reverse('worksheet-create', kwargs = {
                    'project_slug': self.test_section.project.slug,
                    'section_slug': self.test_section.slug}),
                post_data)

        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetDetailView(self):
        """Tests accessing worksheet detail view."""

        response = self.client.get(reverse(
                'worksheet-detail', kwargs = self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetUpdateView(self):
        """Tests updating worksheet without login."""

        response = self.client.get(reverse(
                'worksheet-update', kwargs = self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetUpdateView_with_login(self):
        """Tests updating worksheet with login."""

        status = self.client.login(username='sonlinux', password='password')
        self.assertTrue(status)
        response = self.client.get(reverse(
            'worksheet-update', kwargs=self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_WorksheetModuleQuestionAnswers(self):

        response = self.client.get(reverse('worksheet-module-answers',
                                           kwargs=self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)
