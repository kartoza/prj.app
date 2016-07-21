# coding=utf-8
from base.tests.model_factories import ProjectF
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from core.model_factories import UserF
from permission.tests.model_factories import ProjectAdministratorF, ProjectCollaboratorF
import logging


class PermissionTestViews(TestCase):
    """Tests that Project views work."""

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
        self.admin = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.user = UserF.create(**{
            'username': 'irwan',
            'password': 'password',
            'is_staff': False
        })
        self.user_2 = UserF.create(**{
            'username': 'irwan_2',
            'password': 'password',
            'is_staff': False
        })
        self.test_project_administrator = ProjectAdministratorF.create(user=self.admin)
        self.test_project_collaborator = ProjectCollaboratorF.create(user=self.admin)

    def test_PermissionListView(self):
        client = Client()
        response = client.get(reverse('user-manager', args=('timlinux',)))
        self.assertEqual(response.status_code, 302)

    def test_PermissionListView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('user-manager', args=('timlinux',)))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'permission/permission-list.html', u'base/project_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_PermissionListView_with_login_with_access_different_user(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('user-manager', args=('irwan',)))
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------------
    # ADMINISTRATOR TEST VIEW
    # ---------------------------------------------------------------
    def test_AdministratorCreateView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        project_slug = self.test_project_administrator.project.slug
        response = client.get(reverse('administrator-create', args=(project_slug,)))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'permission/administrator/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_AdministratorCreateView_no_login(self):
        client = Client()
        project_slug = self.test_project_administrator.project.slug
        response = client.get(reverse('administrator-create', args=(project_slug,)))
        self.assertEqual(response.status_code, 302)

    def test_AdministratorCreate_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'project': self.test_project_administrator.project.id,
            'user': self.user.id
        }
        project_slug = self.test_project_administrator.project.slug
        response = client.post(reverse('administrator-create', args=(project_slug,)), post_data)
        self.assertRedirects(response, reverse('user-manager', args=('timlinux',)))

    def test_AdministratorCreate_with_login_and_owner(self):
        client = Client()
        client.login(username='irwan', password='password')
        project = ProjectF.create(owner=self.user)
        post_data = {
            'project': project.id,
            'user': self.admin.id
        }
        project_slug = project.slug
        response = client.post(reverse('administrator-create', args=(project_slug,)), post_data)
        self.assertRedirects(response, reverse('user-manager', args=('irwan',)))

    def test_AdministratorCreate_with_login_and_project_not_own(self):
        client = Client()
        client.login(username='timlinux', password='password')
        project = ProjectF.create(owner=self.user_2)
        client.login(username='irwan', password='password')
        post_data = {
            'project': project.id,
            'user': self.admin.id
        }
        project_slug = project.slug
        response = client.post(reverse('administrator-create', args=(project_slug,)), post_data)
        self.assertEqual(response.status_code, 400)

    def test_AdministratorCreate_no_login(self):
        client = Client()
        post_data = {
            'project': self.test_project_administrator.project.id,
            'user': self.user.id
        }
        project_slug = self.test_project_administrator.project.slug
        response = client.post(reverse('administrator-create', args=(project_slug,)), post_data)
        self.assertEqual(response.status_code, 302)

    def test_AdministratorDeleteView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('administrator-delete', kwargs={
            'pk': self.test_project_administrator.pk
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'permission/administrator/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_AdministratorDeleteView_no_login(self):
        client = Client()
        response = client.get(reverse('administrator-delete', kwargs={
            'pk': self.test_project_administrator.pk
        }))
        self.assertEqual(response.status_code, 302)

    def test_AdministratorDelete_with_login(self):
        client = Client()
        administrator_to_delete = ProjectAdministratorF.create()
        post_data = {
            'pk': administrator_to_delete.pk
        }
        client.login(username='timlinux', password='password')
        response = client.post(reverse('administrator-delete', kwargs={
            'pk': self.test_project_administrator.pk
        }), post_data)
        self.assertRedirects(response, reverse('user-manager', args=('timlinux',)))

    def test_AdministratorDelete_no_login(self):
        client = Client()
        administrator_to_delete = ProjectAdministratorF.create()
        post_data = {
            'pk': administrator_to_delete.pk
        }
        response = client.post(reverse('administrator-delete', kwargs={
            'pk': self.test_project_administrator.pk
        }), post_data)
        self.assertEqual(response.status_code, 302)

    # ---------------------------------------------------------------
    # COLLABORATOR TEST VIEW
    # ---------------------------------------------------------------
    def test_CollaboratorCreateView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        project_slug = self.test_project_collaborator.project.slug
        response = client.get(reverse('collaborator-create', args=(project_slug,)))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'permission/collaborator/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CollaboratorCreateView_no_login(self):
        client = Client()
        project_slug = self.test_project_collaborator.project.slug
        response = client.get(reverse('collaborator-create', args=(project_slug,)))
        self.assertEqual(response.status_code, 302)

    def test_CollaboratorCreate_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'project': self.test_project_collaborator.project.id,
            'user': self.user.id
        }
        project_slug = self.test_project_collaborator.project.slug
        response = client.post(reverse('collaborator-create', args=(project_slug,)), post_data)
        self.assertRedirects(response, reverse('user-manager', args=('timlinux',)))

    def test_CollaboratorCreate_no_login(self):
        client = Client()
        post_data = {
            'project': self.test_project_collaborator.project.id,
            'user': self.user.id
        }
        project_slug = self.test_project_collaborator.project.slug
        response = client.post(reverse('collaborator-create', args=(project_slug,)), post_data)
        self.assertEqual(response.status_code, 302)

    def test_CollaboratorDeleteView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('collaborator-delete', kwargs={
            'pk': self.test_project_collaborator.pk
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'permission/collaborator/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CollaboratorCreate_with_login_and_owner(self):
        client = Client()
        client.login(username='irwan', password='password')
        project = ProjectF.create(owner=self.user)
        post_data = {
            'project': project.id,
            'user': self.admin.id
        }
        project_slug = project.slug
        response = client.post(reverse('collaborator-create', args=(project_slug,)), post_data)
        self.assertRedirects(response, reverse('user-manager', args=('irwan',)))

    def test_CollaboratorCreate_with_login_and_project_not_own(self):
        client = Client()
        client.login(username='timlinux', password='password')
        project = ProjectF.create(owner=self.user_2)
        client.login(username='irwan', password='password')
        post_data = {
            'project': project.id,
            'user': self.admin.id
        }
        project_slug = project.slug
        response = client.post(reverse('collaborator-create', args=(project_slug,)), post_data)
        self.assertEqual(response.status_code, 400)

    def test_CollaboratorDeleteView_no_login(self):
        client = Client()
        response = client.get(reverse('collaborator-delete', kwargs={
            'pk': self.test_project_collaborator.pk
        }))
        self.assertEqual(response.status_code, 302)

    def test_CollaboratorDelete_with_login(self):
        client = Client()
        collaborator_to_delete = ProjectCollaboratorF.create()
        post_data = {
            'pk': collaborator_to_delete.pk
        }
        client.login(username='timlinux', password='password')
        response = client.post(reverse('collaborator-delete', kwargs={
            'pk': self.test_project_collaborator.pk
        }), post_data)
        self.assertRedirects(response, reverse('user-manager', args=('timlinux',)))

    def test_CollaboratorDelete_no_login(self):
        client = Client()
        collaborator_to_delete = ProjectCollaboratorF.create()
        post_data = {
            'pk': collaborator_to_delete.pk
        }
        response = client.post(reverse('collaborator-delete', kwargs={
            'pk': self.test_project_collaborator.pk
        }), post_data)
        self.assertEqual(response.status_code, 302)
