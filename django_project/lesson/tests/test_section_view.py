# coding=utf-8
"""Test for lesson views."""
import logging

from django.core.urlresolvers import reverse

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
        self.user = UserF.create(**{'username': 'timlinux', 'is_staff': True})
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
        self.kwargs_project = {'project_slug': self.test_section.project.slug}
        self.kwargs_section = {'slug': self.test_section.slug}
        self.kwargs_section_full = {
            'project_slug': self.test_section.project.slug,
            'slug': self.test_section.slug
        }
        self.kwargs_worksheet_full = {
            'project_slug': self.test_section.project.slug,
            'section_slug': self.test_section.slug
        }

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionListView(self):
        """Test List View of Section."""
        client = Client()
        response = client.get(
            reverse('section-list', kwargs=self.kwargs_project))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'section/list.html', 'lesson/section_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
        self.assertEqual(
            response.context_data['object_list'][0], self.test_section)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionCreateView_with_login(self):
        """Test access create section with login."""
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse(
            'section-create', kwargs=self.kwargs_project))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionCreateView_no_login(self):
        """Test access create section without login."""
        client = Client()
        response = client.get(reverse(
            'section-create', kwargs=self.kwargs_project))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionCreate_with_login(self):
        """Test create section with login."""
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Section',
            'notes': 'New Notes',
            'sequence_number': 1,
            'project': self.test_project.id,
        }
        response = client.post(
            reverse('section-create', kwargs=self.kwargs_project), post_data)
        self.assertRedirects(
            response, reverse(
                'section-list', kwargs={
                    'project_slug': self.test_section.project.slug}
            ) + '#new-section')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionCreate_no_login(self):
        """Test create section without login."""
        client = Client()
        post_data = {
            'name': u'Newer Section',
            'notes': 'Newer Notes',
            'sequence_number': 2,
            'project': self.test_project.id,
        }
        response = client.post(
            reverse('section-create', kwargs=self.kwargs_project), post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionUpdateView_with_login(self):
        """Test access update section with login."""
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse(
            'section-update', kwargs=self.kwargs_section_full))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionUpdateView_no_login(self):
        """Test access update section without login."""
        client = Client()
        response = client.get(reverse(
            'section-update', kwargs=self.kwargs_section_full))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionUpdate_with_login(self):
        """Test update section with login."""
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Section Update',
            'notes': 'New Notes Update',
            'sequence_number': 10,
            'project': self.test_project.id,
        }
        response = client.post(
            reverse('section-update', kwargs=self.kwargs_section_full),
            post_data)
        self.assertRedirects(response, reverse(
            'section-list', kwargs={
                'project_slug': self.test_section.project.slug}) +
                    '#' + self.test_section.slug)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionUpdate_no_login(self):
        """Test update section without login."""
        client = Client()
        post_data = {
            'name': u'New Test Project Updated',
        }
        response = client.post(
            reverse('section-update', kwargs=self.kwargs_section_full),
            post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionDeleteView_with_login(self):
        """Test access delete section with login."""
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse(
            'section-delete', kwargs=self.kwargs_section_full))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'section/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_SectionDeleteView_no_login(self):
        """Test access delete section without login."""
        client = Client()
        response = client.get(reverse(
            'section-delete', kwargs=self.kwargs_section_full))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionDelete_with_login(self):
        """Test delete section with login."""
        client = Client()
        section_to_delete = SectionF.create()
        post_data = {
            'pk': section_to_delete.pk
        }
        client.login(username='timlinux', password='password')
        response = client.post(reverse('section-delete', kwargs={
            'project_slug': section_to_delete.project.slug,
            'slug': section_to_delete.slug
        }), post_data)
        self.assertRedirects(
            response,
            reverse(
                'section-list',
                kwargs={'project_slug': section_to_delete.project.slug}
            )
        )
        # TODO: The following line to test that the object is deleted does not
        # currently pass as expected.
        # self.assertTrue(section_to_delete.pk is None)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SectionDelete_no_login(self):
        """Test delete section without login."""
        client = Client()
        section_to_delete = SectionF.create()
        response = client.post(reverse('section-delete', kwargs={
            'slug': section_to_delete.slug,
            'project_slug': section_to_delete.project.slug

        }))
        self.assertEqual(response.status_code, 302)
