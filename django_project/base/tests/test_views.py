# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from base.tests.model_factories import ProjectF
from core.model_factories import UserF
import logging


class TestViews(TestCase):
    """Tests that Project views work."""

    def setUp(self):
        """
        Setup before each test
        """
        logging.disable(logging.CRITICAL)
        self.test_project = ProjectF.create()
        self.unapproved_project = ProjectF.create(approved=False)
        self.my_user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def test_ProjectListView(self):
        my_client = Client()
        my_response = my_client.get(reverse('home'))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'project/list.html', u'base/project_list.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)
        self.assertEqual(my_response.context_data['object_list'][0],
                         self.test_project)

    def test_ProjectCreateView_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('project-create'))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'project/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_ProjectCreateView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('project-create'))
        self.assertEqual(my_response.status_code, 404)

    def test_ProjectCreate_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Project',
            'owner': self.my_user.id
        }
        my_response = my_client.post(reverse('project-create'), post_data)
        self.assertRedirects(my_response, reverse('pending-project-list'))

    def test_ProjectCreate_no_login(self):
        my_client = Client()
        post_data = {
            'name': u'New Test Project'
        }
        my_response = my_client.post(reverse('project-create'), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_ProjectUpdateView_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('project-update', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'project/update.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_ProjectUpdateView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('project-update', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_ProjectUpdate_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Project Updated',
            'owner': self.my_user.id
        }
        my_response = my_client.post(reverse('project-update', kwargs={
            'slug': self.test_project.slug
        }), post_data)
        self.assertRedirects(my_response, reverse('project-detail', kwargs={
            'slug': self.test_project.slug
        }))

    def test_ProjectUpdate_no_login(self):
        my_client = Client()
        post_data = {
            'name': u'New Test Project Updated',
            'owner': self.my_user.id
        }
        my_response = my_client.post(reverse('project-update', kwargs={
            'slug': self.test_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_ProjectDetailView(self):
        my_client = Client()
        my_response = my_client.get(reverse('project-detail', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'project/detail.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_ProjectDeleteView_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('project-delete', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'project/delete.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_ProjectDeleteView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('project-delete', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_ProjectDelete_with_login(self):
        my_client = Client()
        project_to_delete = ProjectF.create()
        post_data = {
            'pk': project_to_delete.pk
        }
        my_client.login(username='timlinux', password='password')
        my_response = my_client.post(reverse('project-delete', kwargs={
            'slug': project_to_delete.slug
        }), post_data)
        self.assertRedirects(my_response, reverse('project-list'))
        # TODO: The following line to test that the object is deleted does not
        # currently pass as expected.
        # self.assertTrue(project_to_delete.pk is None)

    def test_ProjectDelete_no_login(self):
        my_client = Client()
        project_to_delete = ProjectF.create()
        my_response = my_client.post(reverse('project-delete', kwargs={
            'slug': project_to_delete.slug
        }))
        self.assertEqual(my_response.status_code, 302)
