# coding: utf-8
"""Unit tests for worksheet views."""

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__copyright__ = 'kartoza.com'


import logging
from django.test import TestCase, override_settings, Client

from base.tests.model_factories import ProjectF
from core.model_factories import UserF
from lesson.tests.model_factories import SectionF


class TestViews(TestCase):
    """Tests that Lesson Section views work."""

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
        self.user = UserF.create(**{'username': 'sonlinux', 'is_staff': True})
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
        self.test_section = SectionF.create()
        self.kwargs_pk = {'pk': self.test_section.pk}
        self.kwargs_section = {'section_slug': self.test_section.slug}
        self.kwargs_project = {'project_slug': self.test_section.project.slug}
        self.kwargs_ = {'section_slug': self.test_section.slug}
        self.kwargs_section_full = {
            'project_slug': self.test_section.project.slug,
            'slug': self.test_section.slug
        }
        self.kwargs_worksheet_full = {
            'pk': self.test_section.pk,
            'project_slug': self.test_section.project.slug,
            'section_slug': self.test_section.slug}

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_WorksheetModuleQuestionAnswers_with_no_login(self):
        client = Client()

        response = client.get('worksheet-module-answers', kwargs={
            'project_slug': self.kwargs_project,
            'section_slug': self.kwargs_section,
            'pk': self.kwargs_pk})
        self.assertEqual(response.status_code, 404)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetModuleQuestionAnswers_with_login(self):

        client = Client()
        status = client.login(username = 'sonlinux', password = 'password')
        self.assertTrue(status)

        response = client.get('worksheet-module-answers', kwargs = {
            'project_slug': self.kwargs_project,
            'section_slug': self.kwargs_section,
            'pk': int(2)})
        self.assertEqual(response.status_code, 404)
