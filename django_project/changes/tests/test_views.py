# coding=utf-8
# flake8: noqa

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from base.tests.model_factories import ProjectF
from changes.tests.model_factories import (
    CategoryF,
    EntryF,
    VersionF,
    SponsorshipLevelF,
    SponsorF,
    SponsorshipPeriodF)
from core.model_factories import UserF
import logging


class TestCategoryViews(TestCase):
    """Tests that Category views work."""

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
        self.my_project = ProjectF.create()
        self.my_category = CategoryF.create(project=self.my_project)
        self.my_user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.my_project.delete()
        self.my_category.delete()
        self.my_user.delete()

    def test_CategoryListView(self):

        my_response = self.client.get(reverse('category-list', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'category/list.html', u'changes/category_list.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)
        self.assertEqual(my_response.context_data['object_list'][0],
                         self.my_category)

    def test_CategoryCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('category-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'category/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_CategoryCreateView_no_login(self):

        my_response = self.client.get(reverse('category-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_CategoryCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Category',
            'project': self.my_project.id,
            'sort_number': 0
        }
        my_response = self.client.post(reverse('category-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertRedirects(
            my_response,
            reverse(
                'pending-category-list',
                kwargs={'project_slug': self.my_project.slug}))

    def test_CategoryCreate_no_login(self):

        post_data = {
            'name': u'New Test Category'
        }
        my_response = self.client.post(reverse('category-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_CategoryDetailView(self):

        my_response = self.client.get(reverse('category-detail', kwargs={
            'slug': self.my_category.slug,
            'project_slug': self.my_category.project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'category/detail.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_CategoryDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('category-delete', kwargs={
            'slug': self.my_category.slug,
            'project_slug': self.my_category.project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'category/delete.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_CategoryDeleteView_no_login(self):

        my_response = self.client.get(reverse('category-delete', kwargs={
            'slug': self.my_category.slug,
            'project_slug': self.my_category.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_CategoryDelete_with_login(self):

        category_to_delete = CategoryF.create(project=self.my_project)
        self.client.login(username='timlinux', password='password')
        my_response = self.client.post(reverse('category-delete', kwargs={
            'slug': category_to_delete.slug,
            'project_slug': category_to_delete.project.slug
        }), {})
        self.assertRedirects(my_response, reverse('category-list', kwargs={
            'project_slug': self.my_project.slug
        }))
        # TODO: The following line to test that
        # the object is deleted does not currently pass as expected.
        # self.assertTrue(category_to_delete.pk is None)

    def test_CategoryDelete_no_login(self):

        category_to_delete = CategoryF.create()
        my_response = self.client.post(reverse('category-delete', kwargs={
            'slug': category_to_delete.slug,
            'project_slug': self.my_category.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)


class TestEntryViews(TestCase):
    """Tests that Entry views work."""

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
        self.my_project = ProjectF.create(
                name='testproject')
        self.my_version = VersionF.create(
                project=self.my_project,
                name='1.0.1')
        self.my_category = CategoryF.create(
                project=self.my_project,
                name='testcategory')
        self.my_entry = EntryF.create(
            category=self.my_category,
            version=self.my_version,
            title='testentry',
            approved=True)
        self.my_user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.my_project.delete()
        self.my_version.delete()
        self.my_category.delete()
        self.my_entry.delete()
        self.my_user.delete()

    def test_EntryListView(self):
        """Test entry list view."""
        my_response = self.client.get(reverse('entry-list', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_entry.version.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'entry/list.html', u'changes/entry_list.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)
        self.assertEqual(my_response.context_data['object_list'][0],
                         self.my_entry)

    def test_EntryCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('entry-create', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_version.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'entry/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_EntryCreateView_no_login(self):

        my_response = self.client.get(reverse('entry-create', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_version.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_EntryCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'title': u'New Test Entry',
            'version': self.my_version.id,
            'category': self.my_category.id,
            'author': self.my_user.id
        }
        my_response = self.client.post(reverse('entry-create', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_version.slug
        }), post_data)
        self.assertRedirects(
            my_response, reverse('pending-entry-list', kwargs={
                'project_slug': self.my_project.slug,
                'version_slug': self.my_version.slug
        }))

    def test_EntryCreate_no_login(self):

        post_data = {
            'title': u'New Test Entry',
            'version': self.my_version.id,
            'category': self.my_category.id
        }
        my_response = self.client.post(reverse('entry-create', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_version.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_EntryUpdateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('entry-update', kwargs={
            'pk': self.my_entry.id
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'entry/update.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_EntryUpdateView_no_login(self):

        my_response = self.client.get(reverse('entry-update', kwargs={
            'pk': self.my_entry.id
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_EntryUpdate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'title': u'New Test Entry Updated',
            'version': self.my_version.id,
            'category': self.my_category.id,
            'author': self.my_user.id
        }
        my_response = self.client.post(reverse('entry-update', kwargs={
            'pk': self.my_entry.id
        }), post_data)
        self.assertRedirects(
            my_response, reverse('pending-entry-list', kwargs={
                'project_slug': self.my_project.slug,
                'version_slug': self.my_version.slug
        }))

    def test_EntryUpdate_no_login(self):

        post_data = {
            'title': u'New Test Entry Updated',
            'version': self.my_version.id,
            'category': self.my_category.id
        }
        my_response = self.client.post(reverse('entry-update', kwargs={
            'pk': self.my_entry.id
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_EntryDetailView(self):
        """Test the entry detail view."""
        # Verify our entry exists
        self.assertTrue(self.my_entry.approved)

        my_url = reverse('entry-detail', kwargs={
            'pk': self.my_entry.id
        })
        my_response = self.client.get(my_url)
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'entry/detail.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_EntryDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('entry-delete', kwargs={
            'pk': self.my_entry.id
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'entry/delete.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_EntryDeleteView_no_login(self):

        my_response = self.client.get(reverse('entry-delete', kwargs={
            'pk': self.my_entry.id
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_EntryDelete_with_login(self):

        entry_to_delete = EntryF.create(
            category=self.my_category,
            version=self.my_version)
        self.client.login(username='timlinux', password='password')
        my_response = self.client.post(reverse('entry-delete', kwargs={
            'pk': entry_to_delete.id
        }), {})
        self.assertRedirects(my_response, reverse('entry-list', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_version.slug
        }))
        # TODO: The following line to test that the object is deleted does not
        # currently pass as expected.
        # self.assertTrue(entry_to_delete.pk is None)

    def test_EntryDelete_no_login(self):

        entry_to_delete = EntryF.create(
            category=self.my_category,
            version=self.my_version)
        my_response = self.client.post(reverse('entry-delete', kwargs={
            'pk': entry_to_delete.id
        }))
        self.assertEqual(my_response.status_code, 302)


class TestVersionViews(TestCase):
    """Tests that Version views work."""

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
        self.my_project = ProjectF.create(name='testproject')
        self.my_version = VersionF.create(
                project=self.my_project,
                name='1.0.1')
        self.my_category = CategoryF.create(
                project=self.my_project,
                name='testcategory')

        self.my_user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.my_project.delete()
        self.my_version.delete()
        self.my_category.delete()
        self.my_user.delete()

    def test_VersionListView(self):

        my_response = self.client.get(reverse('version-list', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'version/list.html', u'changes/version_list.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)
        self.assertEqual(my_response.context_data['object_list'][0],
                         self.my_version)

    def test_VersionCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('version-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'version/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_VersionCreateView_no_login(self):

        my_response = self.client.get(reverse('version-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_VersionCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'project': self.my_project.id,
            'name': u'1.8.1',
            'description': u'This is a test description',
            'author': self.my_user.id
        }
        my_response = self.client.post(reverse('version-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertRedirects(
            my_response, reverse('pending-version-list', kwargs={
                'project_slug': self.my_project.slug})
        )

    def test_VersionCreate_no_login(self):

        post_data = {
            'project': self.my_project.id,
            'name': u'New Test Version',
            'description': u'This is a test description'
        }
        my_response = self.client.post(reverse('version-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_VersionUpdateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('version-update', kwargs={
            'project_slug': self.my_version.project.slug,
            'slug': self.my_version.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'version/update.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_VersionUpdateView_no_login(self):

        my_response = self.client.get(reverse('version-update', kwargs={
            'project_slug': self.my_version.project.slug,
            'slug': self.my_version.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_VersionUpdate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'project': self.my_project.id,
            'name': u'1.5.1',
            'description': u'This is a test description',
            'author': self.my_user.id
        }
        my_response = self.client.post(reverse('version-update', kwargs={
            'project_slug': self.my_version.project.slug,
            'slug': self.my_version.slug
        }), post_data)
        self.assertRedirects(my_response, reverse('version-list', kwargs={
            'project_slug': self.my_project.slug
        }))

    def test_VersionUpdate_no_login(self):

        post_data = {
            'project': self.my_project.id,
            'name': u'New Test Version',
            'description': u'This is a test description'
        }
        my_response = self.client.post(reverse('version-update', kwargs={
            'project_slug': self.my_version.project.slug,
            'slug': self.my_version.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_VersionDetailView(self):

        my_response = self.client.get(reverse('version-detail', kwargs={
            'slug': self.my_version.slug,
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'version/detail.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_VersionDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('version-delete', kwargs={
            'slug': self.my_version.slug,
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'version/delete.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_VersionDeleteView_no_login(self):

        my_response = self.client.get(reverse('version-delete', kwargs={
            'slug': self.my_version.slug,
            'project_slug': self.my_version.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_VersionDelete_with_login(self):

        version_to_delete = VersionF.create(
                project=self.my_project,
                name='8.1.1')
        post_data = {
            'pk': version_to_delete.pk
        }
        self.client.login(username='timlinux', password='password')
        my_response = self.client.post(reverse('version-delete', kwargs={
            'slug': version_to_delete.slug,
            'project_slug': version_to_delete.project.slug
        }), post_data)
        self.assertRedirects(my_response, reverse('version-list', kwargs={
            'project_slug': self.my_project.slug
        }))
        # TODO: The following line to test that the object is deleted does
        # not currently pass as expected.
        # self.assertTrue(version_to_delete.pk is None)

    def test_VersionDelete_no_login(self):

        version_to_delete = VersionF.create(
                project=self.my_project,
                name='2.0.1')
        my_response = self.client.post(reverse('version-delete', kwargs={
            'slug': version_to_delete.slug,
            'project_slug': self.my_version.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)


class TestSponsorshipLevelViews(TestCase):
    """Tests that SponsorshipLevel views work."""

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
        self.my_project = ProjectF.create()
        self.my_sponsorshiplevel = SponsorshipLevelF.create(project=self.my_project)
        self.my_user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.my_project.delete()
        self.my_sponsorshiplevel.delete()
        self.my_user.delete()

    def test_SponsorshipLevelListView(self):

        my_response = self.client.get(reverse('sponsorshiplevel-list', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'sponsorship_level/list.html', u'changes/sponsorshiplevel_list.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)
        self.assertEqual(my_response.context_data['object_list'][0],
                         self.my_sponsorshiplevel)

    def test_SponsorshipLevelCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('sponsorshiplevel-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'sponsorship_level/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_SponsorshipLevelCreateView_no_login(self):

        my_response = self.client.get(reverse('sponsorshiplevel-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorshipLevelCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Sponsorship Level',
            'project': self.my_project.id,
            'sort_number': 0
        }
        my_response = self.client.post(reverse('sponsorshiplevel-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 200)

    def test_SponsorshipLevelCreate_no_login(self):

        post_data = {
            'name': u'New Test Sponsorship Level'
        }
        my_response = self.client.post(reverse('sponsorshiplevel-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorshipLevelDetailView(self):

        my_response = self.client.get(reverse('sponsorshiplevel-detail', kwargs={
            'slug': self.my_sponsorshiplevel.slug,
            'project_slug': self.my_sponsorshiplevel.project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'sponsorship_level/detail.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_SponsorshipLevelDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('sponsorshiplevel-delete', kwargs={
            'slug': self.my_sponsorshiplevel.slug,
            'project_slug': self.my_sponsorshiplevel.project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'sponsorship_level/delete.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_SponsorshipLevelDeleteView_no_login(self):

        my_response = self.client.get(reverse('sponsorshiplevel-delete', kwargs={
            'slug': self.my_sponsorshiplevel.slug,
            'project_slug': self.my_sponsorshiplevel.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorshipLevelDelete_with_login(self):

        sponsorshiplevel_to_delete = SponsorshipLevelF.create(project=self.my_project)
        self.client.login(username='timlinux', password='password')
        my_response = self.client.post(reverse('sponsorshiplevel-delete', kwargs={
            'slug': sponsorshiplevel_to_delete.slug,
            'project_slug': sponsorshiplevel_to_delete.project.slug
        }), {})
        self.assertRedirects(my_response, reverse('sponsorshiplevel-list', kwargs={
            'project_slug': self.my_project.slug
        }))

    def test_SponsorshipLevelDelete_no_login(self):

        sponsorshiplevel_to_delete = SponsorshipLevelF.create()
        my_response = self.client.post(reverse('sponsorshiplevel-delete', kwargs={
            'slug': sponsorshiplevel_to_delete.slug,
            'project_slug': self.my_sponsorshiplevel.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)


class TestSponsorViews(TestCase):
    """Tests that Sponsor views work."""

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
        self.my_project = ProjectF.create()
        self.my_sponsor = SponsorF.create(project=self.my_project)
        self.my_user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.my_project.delete()
        self.my_sponsor.delete()
        self.my_user.delete()

    def test_SponsorListView(self):

        my_response = self.client.get(reverse('sponsor-list', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)

    def test_SponsorCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('sponsor-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'sponsor/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_SponsorCreateView_no_login(self):

        my_response = self.client.get(reverse('sponsor-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Sponsor',
            'project': self.my_project.id,
            'sort_number': 0
        }
        my_response = self.client.post(reverse('sponsor-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 200)

    def test_SponsorCreate_no_login(self):

        post_data = {
            'name': u'New Test Sponsor'
        }
        my_response = self.client.post(reverse('sponsor-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('sponsor-delete', kwargs={
            'slug': self.my_sponsor.slug,
            'project_slug': self.my_sponsor.project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'sponsor/delete.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_SponsorDeleteView_no_login(self):

        my_response = self.client.get(reverse('sponsor-delete', kwargs={
            'slug': self.my_sponsor.slug,
            'project_slug': self.my_sponsor.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorDelete_with_login(self):

        sponsor_to_delete = SponsorF.create(project=self.my_project)
        self.client.login(username='timlinux', password='password')
        my_response = self.client.post(reverse('sponsor-delete', kwargs={
            'slug': sponsor_to_delete.slug,
            'project_slug': sponsor_to_delete.project.slug
        }), {})
        self.assertRedirects(my_response, reverse('sponsor-list', kwargs={
            'project_slug': self.my_project.slug
        }))

    def test_SponsorDelete_no_login(self):

        sponsor_to_delete = SponsorF.create()
        my_response = self.client.post(reverse('sponsor-delete', kwargs={
            'slug': sponsor_to_delete.slug,
            'project_slug': self.my_sponsor.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)


class TestSponsorshipPeriodViews(TestCase):
    """Tests that SponsorshipPeriod views work."""

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
        self.my_project = ProjectF.create(
                name='testproject')
        self.my_sponsor = SponsorF.create(
                project=self.my_project,
                name='Kartoza')
        self.my_sponsorship_level = SponsorshipLevelF.create(
                project=self.my_project,
                name='Gold')
        self.my_sponsorship_period = SponsorshipPeriodF.create(
            sponsor=self.my_sponsor,
            sponsorshiplevel=self.my_sponsorship_level,
            approved=True)
        self.my_user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.my_project.delete()
        self.my_sponsor.delete()
        self.my_sponsorship_level.delete()
        self.my_sponsorship_period.delete()
        self.my_user.delete()

    def test_SponsorshipPeriodListView(self):
        """Test SponsorshipPeriod list view."""
        my_response = self.client.get(reverse('sponsorshipperiod-list', kwargs={
            'project_slug': self.my_project.slug,
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'sponsorship_period/list.html', u'changes/sponsorshipperiod_list.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_SponsorshipPeriodCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('sponsorshipperiod-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'sponsorship_period/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_SponsorshipPeriodCreateView_no_login(self):

        my_response = self.client.get(reverse('sponsorshipperiod-create', kwargs={
            'project_slug': self.my_project.slug,
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorshipPeriodCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'sponsor': self.my_sponsor.id,
            'sponsorshiplevel': self.my_sponsorship_level.id,
            'author': self.my_user.id
        }
        my_response = self.client.post(reverse('sponsorshipperiod-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 200)

    def test_SponsorshipPeriodCreate_no_login(self):

        post_data = {
            'sponsor': self.my_sponsor.id,
            'sponsorship_level': self.my_sponsorship_level.id
        }
        my_response = self.client.post(reverse('sponsorshipperiod-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorshipPeriodUpdateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        my_response = self.client.get(reverse('sponsorshipperiod-update', kwargs={
            'slug': self.my_sponsorship_period.slug,
            'project_slug': self.my_project.slug

        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'sponsorship_period/update.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_SponsorshipPeriodUpdateView_no_login(self):

        my_response = self.client.get(reverse('sponsorshipperiod-update', kwargs={
            'slug': self.my_sponsorship_period.slug,
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorshipPeriodUpdate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'sponsor': self.my_sponsor.id,
            'sponsorshiplevel': self.my_sponsorship_level.id,
            'author': self.my_user.id
        }
        my_response = self.client.post(reverse('sponsorshipperiod-update', kwargs={
            'project_slug': self.my_project.slug,
            'slug': self.my_sponsorship_period.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 200)

    def test_SponsorshipPeriodUpdate_no_login(self):

        post_data = {
            'sponsor': self.my_sponsor.id,
            'sponsorshiplevel': self.my_sponsorship_level.id
        }
        my_response = self.client.post(reverse('sponsorshipperiod-update', kwargs={
            'slug': self.my_sponsorship_period.slug,
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorshipPeriodDeleteView_no_login(self):

        my_response = self.client.get(reverse('sponsorshipperiod-delete', kwargs={
            'project_slug': self.my_project.slug,
            'slug': self.my_sponsorship_period.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_SponsorshipPeriodDelete_no_login(self):

        my_response = self.client.post(reverse('sponsorshipperiod-delete', kwargs={
            'project_slug': self.my_project.slug,
            'slug': self.my_sponsorship_period.slug
        }))
        self.assertEqual(my_response.status_code, 302)
