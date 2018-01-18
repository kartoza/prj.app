# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.test.client import Client
from base.tests.model_factories import ProjectF, OrganisationF
from core.model_factories import UserF
import logging


class TestViews(TestCase):
    """Tests that Project views work."""

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
        self.user = UserF.create(**{
            'username': 'timlinux',
            'is_staff': True
        })
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

        self.test_project = ProjectF.create()
        self.unapproved_project = ProjectF.create(approved=False)
        self.test_organisation = OrganisationF.create()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectListView(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'project/list.html', u'base/project_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
        self.assertEqual(response.context_data['object_list'][0],
                         self.test_project)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectCreateView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'project/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectCreateView_no_login(self):
        client = Client()
        response = client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectCreate_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Project',
            'owner': self.user.id,
            'project_url': 'http://foo.org',
            'screenshots-TOTAL_FORMS': 5,
            'screenshots-INITIAL_FORMS': 0,
            'organisation': self.test_organisation.id,
        }
        response = client.post(reverse('project-create'), post_data)
        self.assertRedirects(response, reverse('pending-project-list'))

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectCreate_no_login(self):
        client = Client()
        post_data = {
            'name': u'New Test Project'
        }
        response = client.post(reverse('project-create'), post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectUpdateView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('project-update', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'project/update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectUpdateView_no_login(self):
        client = Client()
        response = client.get(reverse('project-update', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectUpdate_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Project Updated',
            'owner': self.user.id,
            'screenshots-TOTAL_FORMS': 5,
            'screenshots-INITIAL_FORMS': 0,
            'organisation': self.test_organisation.id,
        }
        response = client.post(reverse('project-update', kwargs={
            'slug': self.test_project.slug
        }), post_data)
        self.assertRedirects(response, reverse('project-detail', kwargs={
            'slug': self.test_project.slug
        }))

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectUpdate_no_login(self):
        client = Client()
        post_data = {
            'name': u'New Test Project Updated',
            'owner': self.user.id
        }
        response = client.post(reverse('project-update', kwargs={
            'slug': self.test_project.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectDetailView(self):
        client = Client()
        response = client.get(reverse('project-detail', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'project/new_detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectDeleteView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('project-delete', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'project/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_ProjectDeleteView_no_login(self):
        client = Client()
        response = client.get(reverse('project-delete', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectDelete_with_login(self):
        client = Client()
        project_to_delete = ProjectF.create()
        post_data = {
            'pk': project_to_delete.pk
        }
        client.login(username='timlinux', password='password')
        response = client.post(reverse('project-delete', kwargs={
            'slug': project_to_delete.slug
        }), post_data)
        self.assertRedirects(response, reverse('project-list'))
        # TODO: The following line to test that the object is deleted does not
        # currently pass as expected.
        # self.assertTrue(project_to_delete.pk is None)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectDelete_no_login(self):
        client = Client()
        project_to_delete = ProjectF.create()
        response = client.post(reverse('project-delete', kwargs={
            'slug': project_to_delete.slug
        }))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_GithubRepoView_no_login(self):
        client = Client()
        response = client.get(reverse('project-delete', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_GithubRepoView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('github-repo-view'))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'github/populate-github.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
