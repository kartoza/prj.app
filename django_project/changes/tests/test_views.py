# coding=utf-8
# flake8: noqa

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from base.tests.model_factories import ProjectF
from changes.tests.model_factories import CategoryF, EntryF, VersionF
from core.model_factories import UserF
import logging


class TestCategoryViews(TestCase):
    """Tests that Category views work."""

    def setUp(self):
        """
        Setup before each test
        """
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
        my_client = Client()
        my_response = my_client.get(reverse('category-list', kwargs={
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
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('category-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'category/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_CategoryCreateView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('category-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_CategoryCreate_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Category',
            'project': self.my_project.id,
            'sort_number': 0
        }
        my_response = my_client.post(reverse('category-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertRedirects(
            my_response,
            reverse(
                'pending-category-list',
                kwargs={'project_slug': self.my_project.slug}))

    def test_CategoryCreate_no_login(self):
        my_client = Client()
        post_data = {
            'name': u'New Test Category'
        }
        my_response = my_client.post(reverse('category-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_CategoryDetailView(self):
        my_client = Client()
        my_response = my_client.get(reverse('category-detail', kwargs={
            'slug': self.my_category.slug,
            'project_slug': self.my_category.project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'category/detail.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_CategoryDeleteView_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('category-delete', kwargs={
            'slug': self.my_category.slug,
            'project_slug': self.my_category.project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'category/delete.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_CategoryDeleteView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('category-delete', kwargs={
            'slug': self.my_category.slug,
            'project_slug': self.my_category.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_CategoryDelete_with_login(self):
        my_client = Client()
        category_to_delete = CategoryF.create(project=self.my_project)
        my_client.login(username='timlinux', password='password')
        my_response = my_client.post(reverse('category-delete', kwargs={
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
        my_client = Client()
        category_to_delete = CategoryF.create()
        my_response = my_client.post(reverse('category-delete', kwargs={
            'slug': category_to_delete.slug,
            'project_slug': self.my_category.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)


class TestEntryViews(TestCase):
    """Tests that Entry views work."""

    def setUp(self):
        """
        Setup before each test
        """
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
            title='testentry')
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

    def test_EntryListView(self):
        my_client = Client()
        my_response = my_client.get(reverse('entry-list', kwargs={
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
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('entry-create', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_version.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'entry/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_EntryCreateView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('entry-create', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_version.slug
        }))
        self.assertEqual(my_response.status_code, 404)

    def test_EntryCreate_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        post_data = {
            'title': u'New Test Entry',
            'version': self.my_version.id,
            'category': self.my_category.id,
            'author': self.my_user.id
        }
        my_response = my_client.post(reverse('entry-create', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_version.slug
        }), post_data)
        self.assertRedirects(
            my_response, reverse('pending-entry-list', kwargs={
                'project_slug': self.my_project.slug,
                'version_slug': self.my_version.slug
        }))

    def test_EntryCreate_no_login(self):
        my_client = Client()
        post_data = {
            'title': u'New Test Entry',
            'version': self.my_version.id,
            'category': self.my_category.id
        }
        my_response = my_client.post(reverse('entry-create', kwargs={
            'project_slug': self.my_project.slug,
            'version_slug': self.my_version.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_EntryUpdateView_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('entry-update', kwargs={
            'pk': self.my_entry.id
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'entry/update.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_EntryUpdateView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('entry-update', kwargs={
            'pk': self.my_entry.id
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_EntryUpdate_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        post_data = {
            'title': u'New Test Entry Updated',
            'version': self.my_version.id,
            'category': self.my_category.id,
            'author': self.my_user.id
        }
        my_response = my_client.post(reverse('entry-update', kwargs={
            'pk': self.my_entry.id
        }), post_data)
        self.assertRedirects(
            my_response, reverse('pending-entry-list', kwargs={
                'project_slug': self.my_project.slug,
                'version_slug': self.my_version.slug
        }))

    def test_EntryUpdate_no_login(self):
        my_client = Client()
        post_data = {
            'title': u'New Test Entry Updated',
            'version': self.my_version.id,
            'category': self.my_category.id
        }
        my_response = my_client.post(reverse('entry-update', kwargs={
            'pk': self.my_entry.id
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_EntryDetailView(self):
        my_client = Client()
        my_response = my_client.get(reverse('entry-detail', kwargs={
            'pk': self.my_entry.id
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'entry/detail.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_EntryDeleteView_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('entry-delete', kwargs={
            'pk': self.my_entry.id
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'entry/delete.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_EntryDeleteView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('entry-delete', kwargs={
            'pk': self.my_entry.id
        }))
        self.assertEqual(my_response.status_code, 404)

    def test_EntryDelete_with_login(self):
        my_client = Client()
        entry_to_delete = EntryF.create(
            category=self.my_category,
            version=self.my_version)
        my_client.login(username='timlinux', password='password')
        my_response = my_client.post(reverse('entry-delete', kwargs={
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
        my_client = Client()
        entry_to_delete = EntryF.create(
            category=self.my_category,
            version=self.my_version)
        my_response = my_client.post(reverse('entry-delete', kwargs={
            'pk': entry_to_delete.id
        }))
        self.assertEqual(my_response.status_code, 302)


class TestVersionViews(TestCase):
    """Tests that Version views work."""

    def setUp(self):
        """
        Setup before each test
        """
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
        my_client = Client()
        my_response = my_client.get(reverse('version-list', kwargs={
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
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('version-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'version/create.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_VersionCreateView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('version-create', kwargs={
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_VersionCreate_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        post_data = {
            'project': self.my_project.id,
            'name': u'1.8.1',
            'description': u'This is a test description',
            'author': self.my_user.id
        }
        my_response = my_client.post(reverse('version-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertRedirects(
            my_response, reverse('pending-version-list', kwargs={
                'project_slug': self.my_project.slug})
        )

    def test_VersionCreate_no_login(self):
        my_client = Client()
        post_data = {
            'project': self.my_project.id,
            'name': u'New Test Version',
            'description': u'This is a test description'
        }
        my_response = my_client.post(reverse('version-create', kwargs={
            'project_slug': self.my_project.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_VersionUpdateView_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('version-update', kwargs={
            'project_slug': self.my_version.project.slug,
            'slug': self.my_version.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'version/update.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_VersionUpdateView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('version-update', kwargs={
            'project_slug': self.my_version.project.slug,
            'slug': self.my_version.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_VersionUpdate_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        post_data = {
            'project': self.my_project.id,
            'name': u'1.5.1',
            'description': u'This is a test description',
            'author': self.my_user.id
        }
        my_response = my_client.post(reverse('version-update', kwargs={
            'project_slug': self.my_version.project.slug,
            'slug': self.my_version.slug
        }), post_data)
        self.assertRedirects(my_response, reverse('version-list', kwargs={
            'project_slug': self.my_project.slug
        }))

    def test_VersionUpdate_no_login(self):
        my_client = Client()
        post_data = {
            'project': self.my_project.id,
            'name': u'New Test Version',
            'description': u'This is a test description'
        }
        my_response = my_client.post(reverse('version-update', kwargs={
            'project_slug': self.my_version.project.slug,
            'slug': self.my_version.slug
        }), post_data)
        self.assertEqual(my_response.status_code, 302)

    def test_VersionDetailView(self):
        my_client = Client()
        my_response = my_client.get(reverse('version-detail', kwargs={
            'slug': self.my_version.slug,
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'version/detail.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_VersionDeleteView_with_login(self):
        my_client = Client()
        my_client.login(username='timlinux', password='password')
        my_response = my_client.get(reverse('version-delete', kwargs={
            'slug': self.my_version.slug,
            'project_slug': self.my_project.slug
        }))
        self.assertEqual(my_response.status_code, 200)
        expected_templates = [
            'version/delete.html'
        ]
        self.assertEqual(my_response.template_name, expected_templates)

    def test_VersionDeleteView_no_login(self):
        my_client = Client()
        my_response = my_client.get(reverse('version-delete', kwargs={
            'slug': self.my_version.slug,
            'project_slug': self.my_version.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)

    def test_VersionDelete_with_login(self):
        my_client = Client()
        version_to_delete = VersionF.create(
                project=self.my_project,
                name='8.1.1')
        post_data = {
            'pk': version_to_delete.pk
        }
        my_client.login(username='timlinux', password='password')
        my_response = my_client.post(reverse('version-delete', kwargs={
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
        my_client = Client()
        version_to_delete = VersionF.create(
                project=self.my_project,
                name='2.0.1')
        my_response = my_client.post(reverse('version-delete', kwargs={
            'slug': version_to_delete.slug,
            'project_slug': self.my_version.project.slug
        }))
        self.assertEqual(my_response.status_code, 302)
