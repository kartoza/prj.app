# coding=utf-8
from django.urls import reverse
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
        self.assertRedirects(response, reverse('home'))

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
            'slug': self.test_project.slug,
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
        self.assertContains(response, '<h3>Lessons</h3>')
        self.assertContains(response, '<h3>Certification</h3>')
        self.assertContains(response, '<h3>Project Teams</h3>')
        self.assertContains(response, '<h3>Release Changelogs</h3>')
        self.assertContains(response, '<h3>Sustaining Members</h3>')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_ProjectDetailView_with_features_not_checked(self):
        self.test_project.is_lessons = False
        self.test_project.is_sustaining_members = False
        self.test_project.is_teams = False
        self.test_project.is_changelogs = False
        self.test_project.is_certification = False
        self.test_project.save()

        client = Client()
        response = client.get(reverse('project-detail', kwargs={
            'slug': self.test_project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'project/new_detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
        self.assertNotContains(response, '<h3>Lessons</h3>')
        self.assertNotContains(response, '<h3>Certification</h3>')
        self.assertNotContains(response, '<h3>Project Teams</h3>')
        self.assertNotContains(response, '<h3>Release Changelogs</h3>')
        self.assertNotContains(response, '<h3>Sustaining Members</h3>')

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


class TestOrganisationCreate(TestCase):
    """Test organisation creation."""
    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """Setting up before each test."""
        self.client = Client()
        self.client.post(
                '/set_language/', data = {'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.user = UserF.create(**{
            'username': 'sonlinux',
            'is_staff': True,
        })

        self.user.set_password('password')
        self.user.save()

        # lets set up a testing project to create organisations from.
        self.test_project = ProjectF.create()
        self.unapproved_project = ProjectF.create(approved=False)
        self.test_organisation = OrganisationF.create()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_oroganisation_create_with_login(self):
        """
        Test that a single logged in user can create multiple organisations.
        """
        client = Client()
        loged_in = client.login(username='sonlinux', password='password')

        # Test client log in.
        self.assertTrue(loged_in)

        expected_templates = [
            'organisation/create.html'
        ]
        response = client.post(reverse('create-organisation'))
        self.assertEqual(response.status_code, 200)

        # Test if get the correct template view after creation.
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_multiple_organisation_create_with_single_login(self):
        """
        Test that a single logged in user can create multiple
        organisations.
        """
        client = Client()
        loged_in = client.login(username='sonlinux', password='password')

        # Test that user is actually loged in.
        self.assertTrue(loged_in)
        post_data_list = [
            'Test organisation creation',
            'Test organisation creation two',
            'Test organisation creation three']

        for post_data in post_data_list:
            response = client.post(reverse('create-organisation'),
                                   {'name': post_data})
            self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_organisation_create_with_no_login(self):
        """Test that no non-authenticated user can create an organisation."""
        client = Client()
        post_data = {
            'name': u'A new test organisation',
        }
        # response = client.post( reverse( 'account_login') , post_data )
        response = client.post(reverse('create-organisation'), post_data)
        self.assertEqual(response.status_code, 302)


class TestOrganisationCreateWithSuperuserPermissions(TestCase):
    """Test organisation creation with a superuser login."""
    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """Setting up before each test."""
        self.client = Client()
        self.client.post(
                '/set_language/', data = {'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.user = UserF.create(**{
            'username': 'sonlinux',
            'is_superuser': True,
        })

        self.user.set_password('password')
        self.user.save()

        # lets set up a testing project to create organisations from.
        self.test_project = ProjectF.create()
        self.unapproved_project = ProjectF.create(approved=False)
        self.test_organisation = OrganisationF.create()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_oroganisation_create_with_superuser(self):
        """
        Test that a superuser login can create multiple organisations.
        """
        client = Client()
        loged_in = client.login(username='sonlinux', password='password')

        # Test client log in.
        self.assertTrue(loged_in)

        expected_templates = [
            'organisation/create.html'
        ]
        response = client.post(reverse('create-organisation'))
        self.assertEqual(response.status_code, 200)

        # Test if get the correct template view after creation.
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_multiple_organisation_create_with_superuser(self):
        """
        Test that a superuser login can create multiple organisations.
        """
        client = Client()
        loged_in = client.login(username='sonlinux', password='password')

        # Test that user is actually loged in.
        self.assertTrue(loged_in)
        post_data_list = [
            'Test organisation creation',
            'Test organisation creation two',
            'Test organisation creation three']

        for post_data in post_data_list:
            response = client.post(reverse('create-organisation'),
                                   {'name': post_data})
            self.assertEqual(response.status_code, 302)


class TestOrganisationCreateWithNoneStaffPermissions(TestCase):
    """Test organisation creation with a none staff user."""
    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """Setting up before each test."""
        self.client = Client()
        self.client.post(
                '/set_language/', data = {'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.user = UserF.create(**{
            'username': 'sonlinux',
            'is_staff': False,
        })

        self.user.set_password('password')
        self.user.save()

        # lets set up a testing project to create organisations from.
        self.test_project = ProjectF.create()
        self.unapproved_project = ProjectF.create(approved=False)
        self.test_organisation = OrganisationF.create()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_oroganisation_create_with_none_staff_login(self):
        """Test that a none staff user can create an organisations."""

        client = Client()
        loged_in = client.login(username='sonlinux', password='password')

        # Test client log in.
        self.assertTrue(loged_in)

        expected_templates = [
            'organisation/create.html'
        ]
        response = client.post(reverse('create-organisation'))
        self.assertEqual(response.status_code, 200)

        # Test if get the correct template view after creation.
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_multiple_organisation_create_with_none_staff_user(self):
        """
        Test that a none staff user can create multiple organisations.
        """
        client = Client()
        loged_in = client.login(username='sonlinux', password='password')

        # Test that user is actually loged in.
        self.assertTrue(loged_in)
        post_data_list = [
            'Test organisation creation',
            'Test organisation creation two',
            'Test organisation creation three']

        for post_data in post_data_list:
            response = client.post(reverse('create-organisation'),
                                   {'name': post_data})
            self.assertEqual(response.status_code, 302)
