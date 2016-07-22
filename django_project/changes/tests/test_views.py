# coding=utf-8
# flake8: noqa

import json
from django.utils.datastructures import MultiValueDict
from django.utils.http import urlencode

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
        self.project = ProjectF.create()
        self.category = CategoryF.create(project=self.project)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.category.delete()
        self.user.delete()

    def test_CategoryListView(self):

        response = self.client.get(reverse('category-list', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_CategoryCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('category-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'category/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CategoryCreateView_no_login(self):

        response = self.client.get(reverse('category-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_CategoryCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Category',
            'project': self.project.id,
            'sort_number': 0
        }
        response = self.client.post(reverse('category-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertRedirects(
            response,
            reverse(
                'pending-category-list',
                kwargs={'project_slug': self.project.slug}))

    def test_CategoryCreate_no_login(self):

        post_data = {
            'name': u'New Test Category'
        }
        response = self.client.post(reverse('category-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_CategoryDetailView(self):

        response = self.client.get(reverse('category-detail', kwargs={
            'slug': self.category.slug,
            'project_slug': self.category.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'category/detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CategoryDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('category-delete', kwargs={
            'slug': self.category.slug,
            'project_slug': self.category.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'category/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CategoryDeleteView_no_login(self):

        response = self.client.get(reverse('category-delete', kwargs={
            'slug': self.category.slug,
            'project_slug': self.category.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_CategoryDelete_with_login(self):

        category_to_delete = CategoryF.create(project=self.project)
        self.client.login(username='timlinux', password='password')
        response = self.client.post(reverse('category-delete', kwargs={
            'slug': category_to_delete.slug,
            'project_slug': category_to_delete.project.slug
        }), {})
        self.assertRedirects(response, reverse('category-list', kwargs={
            'project_slug': self.project.slug
        }))
        # TODO: The following line to test that
        # the object is deleted does not currently pass as expected.
        # self.assertTrue(category_to_delete.pk is None)

    def test_CategoryDelete_no_login(self):

        category_to_delete = CategoryF.create()
        response = self.client.post(reverse('category-delete', kwargs={
            'slug': category_to_delete.slug,
            'project_slug': self.category.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_CategoryOrederView_wiht_login_as_no_staff(self):
        self.user = UserF.create(**{
            'username': 'dimas',
            'password': 'password',
            'is_staff': False
        })
        self.client.login(
            username='dimas',
            password='password')
        response = self.client.get(reverse('category-order', kwargs={
            'project_slug': self.category.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_CategoryOrderView_with_login_as_staff(self):
        self.client.login(
            username='timlinux',
            password='password')
        response = self.client.get(reverse('category-order', kwargs={
            'project_slug': self.category.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'category/order.html', u'changes/entry_list.html'
        ]
        self.assertTrue(response.template_name, expected_templates)

    def test_CategoryOrderView_no_login(self):

        response = self.client.get(reverse('category-order', kwargs={
            'project_slug': self.category.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_CategoryOrder_with_login(self):
        category_to_order = CategoryF.create(
            project=self.project,
            id=2,
            sort_number=1)
        self.client.login(username='timlinux', password='password')
        post_data = [{
            'name': u'New Test Category',
            'id': '2',
            'sort_number': '0'
        }]

        response = self.client.post(reverse('category-submit-order', kwargs={
            'project_slug': self.project.slug
        }), json.dumps(post_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_CategoryOrder_with_no_login(self):
        category_to_order = CategoryF.create(
            project=self.project,
            id=2,
            sort_number=1)
        post_data = [{
            'name': u'New Test Category',
            'id': '2',
            'sort_number': '0'
        }]

        response = self.client.post(reverse('category-submit-order', kwargs={
            'project_slug': self.project.slug
        }), json.dumps(post_data), content_type='application/json')

        self.assertEqual(response.status_code, 302)




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
        self.project = ProjectF.create(
                name='testproject')
        self.version = VersionF.create(
                project=self.project,
                name='1.0.1')
        self.category = CategoryF.create(
                project=self.project,
                name='testcategory')
        self.entry = EntryF.create(
            category=self.category,
            version=self.version,
            title='testentry',
            approved=True)
        self.pending_entry = EntryF.create(
            category=self.category,
            version=self.version,
            title='testentry2',
            approved=False)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.version.delete()
        self.category.delete()
        self.entry.delete()
        self.user.delete()

    def test_EntryListView(self):
        """Test entry list view."""
        response = self.client.get(reverse('entry-list', kwargs={
            'project_slug': self.project.slug,
            'version_slug': self.entry.version.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'entry/list.html', u'changes/entry_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
        self.assertEqual(response.context_data['object_list'][0],
                         self.pending_entry)

    def test_EntryCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('entry-create', kwargs={
            'project_slug': self.project.slug,
            'version_slug': self.version.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'entry/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_EntryCreateView_no_login(self):

        response = self.client.get(reverse('entry-create', kwargs={
            'project_slug': self.project.slug,
            'version_slug': self.version.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_EntryCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'title': u'New Test Entry',
            'version': self.version.id,
            'category': self.category.id,
            'author': self.user.id
        }
        response = self.client.post(reverse('entry-create', kwargs={
            'project_slug': self.project.slug,
            'version_slug': self.version.slug
        }), post_data)
        self.assertRedirects(
            response, reverse('pending-entry-list', kwargs={
                'project_slug': self.project.slug,
                'version_slug': self.version.slug}))

    def test_EntryCreate_no_login(self):

        post_data = {
            'title': u'New Test Entry',
            'version': self.version.id,
            'category': self.category.id
        }
        response = self.client.post(reverse('entry-create', kwargs={
            'project_slug': self.project.slug,
            'version_slug': self.version.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_EntryUpdateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('entry-update', kwargs={
            'pk': self.entry.id
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'entry/update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_EntryUpdateView_no_login(self):

        response = self.client.get(reverse('entry-update', kwargs={
            'pk': self.entry.id
        }))
        self.assertEqual(response.status_code, 302)

    def test_EntryUpdate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'title': u'New Test Entry Updated',
            'version': self.version.id,
            'category': self.category.id,
            'author': self.user.id
        }
        response = self.client.post(reverse('entry-update', kwargs={
            'pk': self.entry.id
        }), post_data)
        self.assertRedirects(
            response, reverse('pending-entry-list', kwargs={
                'project_slug': self.project.slug,
                'version_slug': self.version.slug}))

    def test_EntryUpdate_no_login(self):

        post_data = {
            'title': u'New Test Entry Updated',
            'version': self.version.id,
            'category': self.category.id
        }
        response = self.client.post(reverse('entry-update', kwargs={
            'pk': self.entry.id
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_EntryDetailView(self):
        """Test the entry detail view."""
        # Verify our entry exists
        self.assertTrue(self.entry.approved)

        url = reverse('entry-detail', kwargs={
            'pk': self.entry.id
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'entry/detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_EntryDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('entry-delete', kwargs={
            'pk': self.entry.id
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'entry/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_EntryDeleteView_no_login(self):

        response = self.client.get(reverse('entry-delete', kwargs={
            'pk': self.entry.id
        }))
        self.assertEqual(response.status_code, 302)

    def test_EntryDelete_with_login(self):

        entry_to_delete = EntryF.create(
            category=self.category,
            version=self.version)
        self.client.login(username='timlinux', password='password')
        response = self.client.post(reverse('entry-delete', kwargs={
            'pk': entry_to_delete.id
        }), {})
        self.assertRedirects(response, reverse('entry-list', kwargs={
            'project_slug': self.project.slug,
            'version_slug': self.version.slug
        }))
        # TODO: The following line to test that the object is deleted does not
        # currently pass as expected.
        # self.assertTrue(entry_to_delete.pk is None)

    def test_EntryDelete_no_login(self):

        entry_to_delete = EntryF.create(
            category=self.category,
            version=self.version)
        response = self.client.post(reverse('entry-delete', kwargs={
            'pk': entry_to_delete.id
        }))
        self.assertEqual(response.status_code, 302)

    def test_AllEntryPendingView(self):
        """Test the all pending entry view."""
        # Verify our pending entry exists
        self.assertFalse(self.pending_entry.approved)
        self.client.login(username='timlinux', password='password')
        url = reverse('all-pending-entry-list', kwargs={
            'project_slug': self.project.slug,
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'entry/all-pending-list.html', u'changes/entry_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)



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
        self.project = ProjectF.create(name='testproject')
        self.version = VersionF.create(
                project=self.project,
                name='1.0.1')
        self.category = CategoryF.create(
                project=self.project,
                name='testcategory')

        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.version.delete()
        self.category.delete()
        self.user.delete()

    def test_VersionListView(self):

        response = self.client.get(reverse('version-list', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'version/list.html', u'changes/version_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
        self.assertEqual(response.context_data['object_list'][0],
                         self.version)

    def test_VersionCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('version-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'version/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_VersionCreateView_no_login(self):

        response = self.client.get(reverse('version-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_VersionCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'project': self.project.id,
            'name': u'1.8.1',
            'description': u'This is a test description',
            'author': self.user.id
        }
        response = self.client.post(reverse('version-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertRedirects(
            response, reverse('pending-version-list', kwargs={
                'project_slug': self.project.slug})
        )

    def test_VersionCreate_no_login(self):

        post_data = {
            'project': self.project.id,
            'name': u'New Test Version',
            'description': u'This is a test description'
        }
        response = self.client.post(reverse('version-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_VersionUpdateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('version-update', kwargs={
            'project_slug': self.version.project.slug,
            'slug': self.version.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'version/update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_VersionUpdateView_no_login(self):

        response = self.client.get(reverse('version-update', kwargs={
            'project_slug': self.version.project.slug,
            'slug': self.version.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_VersionUpdate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'project': self.project.id,
            'name': u'1.5.1',
            'description': u'This is a test description',
            'author': self.user.id
        }
        response = self.client.post(reverse('version-update', kwargs={
            'project_slug': self.version.project.slug,
            'slug': self.version.slug
        }), post_data)
        self.assertRedirects(response, reverse('version-list', kwargs={
            'project_slug': self.project.slug
        }))

    def test_VersionUpdate_no_login(self):

        post_data = {
            'project': self.project.id,
            'name': u'New Test Version',
            'description': u'This is a test description'
        }
        response = self.client.post(reverse('version-update', kwargs={
            'project_slug': self.version.project.slug,
            'slug': self.version.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_VersionDetailView(self):

        response = self.client.get(reverse('version-detail', kwargs={
            'slug': self.version.slug,
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'version/detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_VersionDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('version-delete', kwargs={
            'slug': self.version.slug,
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'version/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_VersionDeleteView_no_login(self):

        response = self.client.get(reverse('version-delete', kwargs={
            'slug': self.version.slug,
            'project_slug': self.version.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_VersionDelete_with_login(self):

        version_to_delete = VersionF.create(
                project=self.project,
                name='8.1.1')
        post_data = {
            'pk': version_to_delete.pk
        }
        self.client.login(username='timlinux', password='password')
        response = self.client.post(reverse('version-delete', kwargs={
            'slug': version_to_delete.slug,
            'project_slug': version_to_delete.project.slug
        }), post_data)
        self.assertRedirects(response, reverse('version-list', kwargs={
            'project_slug': self.project.slug
        }))
        # TODO: The following line to test that the object is deleted does
        # not currently pass as expected.
        # self.assertTrue(version_to_delete.pk is None)

    def test_VersionDelete_no_login(self):

        version_to_delete = VersionF.create(
                project=self.project,
                name='2.0.1')
        response = self.client.post(reverse('version-delete', kwargs={
            'slug': version_to_delete.slug,
            'project_slug': self.version.project.slug
        }))
        self.assertEqual(response.status_code, 302)


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
        self.project = ProjectF.create()
        self.sponsorship_level = SponsorshipLevelF.create(project=self.project)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.sponsorship_level.delete()
        self.user.delete()

    def test_SponsorshipLevelListView(self):

        response = self.client.get(reverse('sponsorshiplevel-list', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_level/list.html', u'changes/sponsorshiplevel_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
        self.assertEqual(response.context_data['object_list'][0],
                         self.sponsorship_level)

    def test_SponsorshipLevelCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsorshiplevel-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_level/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_SponsorshipLevelCreateView_no_login(self):

        response = self.client.get(reverse('sponsorshiplevel-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_SponsorshipLevelCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Sponsorship Level',
            'project': self.project.id,
            'sort_number': 0
        }
        response = self.client.post(reverse('sponsorshiplevel-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 200)

    def test_SponsorshipLevelCreate_no_login(self):

        post_data = {
            'name': u'New Test Sponsorship Level'
        }
        response = self.client.post(reverse('sponsorshiplevel-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_SponsorshipLevelDetailView(self):

        response = self.client.get(reverse('sponsorshiplevel-detail', kwargs={
            'slug': self.sponsorship_level.slug,
            'project_slug': self.sponsorship_level.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_level/detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_SponsorshipLevelDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsorshiplevel-delete', kwargs={
            'slug': self.sponsorship_level.slug,
            'project_slug': self.sponsorship_level.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_level/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_SponsorshipLevelDeleteView_no_login(self):

        response = self.client.get(reverse('sponsorshiplevel-delete', kwargs={
            'slug': self.sponsorship_level.slug,
            'project_slug': self.sponsorship_level.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_SponsorshipLevelDelete_with_login(self):

        sponsorship_level_to_delete = SponsorshipLevelF.create(
                project=self.project)
        self.client.login(username='timlinux', password='password')
        response = self.client.post(reverse('sponsorshiplevel-delete', kwargs={
            'slug': sponsorship_level_to_delete.slug,
            'project_slug': sponsorship_level_to_delete.project.slug
        }), {})
        self.assertRedirects(response, reverse('sponsorshiplevel-list', kwargs={
            'project_slug': self.project.slug
        }))

    def test_SponsorshipLevelDelete_no_login(self):

        sponsorshiplevel_to_delete = SponsorshipLevelF.create()
        response = self.client.post(reverse('sponsorshiplevel-delete', kwargs={
            'slug': sponsorshiplevel_to_delete.slug,
            'project_slug': self.sponsorship_level.project.slug
        }))
        self.assertEqual(response.status_code, 302)


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
        self.project = ProjectF.create()
        self.sponsor = SponsorF.create(project=self.project)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.sponsor.delete()
        self.user.delete()

    def test_SponsorListView(self):

        response = self.client.get(reverse('sponsor-list', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)

    def test_SponsorWorldMapView(self):

        response = self.client.get(reverse('sponsor-world-map', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsor/world-map.html',
            u'changes/sponsorshipperiod_list.html'
        ]
        self.assertEqual(expected_templates, response.template_name)

    def test_SponsorCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsor-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsor/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_SponsorCreateView_no_login(self):

        response = self.client.get(reverse('sponsor-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_SponsorCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Sponsor',
            'project': self.project.id,
            'sort_number': 0
        }
        response = self.client.post(reverse('sponsor-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 200)

    def test_SponsorCreate_no_login(self):

        post_data = {
            'name': u'New Test Sponsor'
        }
        response = self.client.post(reverse('sponsor-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_SponsorDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsor-delete', kwargs={
            'slug': self.sponsor.slug,
            'project_slug': self.sponsor.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsor/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_SponsorDeleteView_no_login(self):

        response = self.client.get(reverse('sponsor-delete', kwargs={
            'slug': self.sponsor.slug,
            'project_slug': self.sponsor.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_SponsorDelete_with_login(self):

        sponsor_to_delete = SponsorF.create(project=self.project)
        self.client.login(username='timlinux', password='password')
        response = self.client.post(reverse('sponsor-delete', kwargs={
            'slug': sponsor_to_delete.slug,
            'project_slug': sponsor_to_delete.project.slug
        }), {})
        self.assertRedirects(response, reverse('sponsor-list', kwargs={
            'project_slug': self.project.slug
        }))

    def test_SponsorDelete_no_login(self):

        sponsor_to_delete = SponsorF.create()
        response = self.client.post(reverse('sponsor-delete', kwargs={
            'slug': sponsor_to_delete.slug,
            'project_slug': self.sponsor.project.slug
        }))
        self.assertEqual(response.status_code, 302)


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
        self.project = ProjectF.create(
                name='testproject')
        self.sponsor = SponsorF.create(
                project=self.project,
                name='Kartoza')
        self.sponsorship_level = SponsorshipLevelF.create(
                project=self.project,
                name='Gold')
        self.sponsorship_period = SponsorshipPeriodF.create(
            sponsor=self.sponsor,
            sponsorship_level=self.sponsorship_level,
            approved=True)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.sponsor.delete()
        self.sponsorship_level.delete()
        self.sponsorship_period.delete()
        self.user.delete()

    def test_SponsorshipPeriodListView(self):
        """Test SponsorshipPeriod list view."""
        response = self.client.get(reverse('sponsorshipperiod-list', kwargs={
            'project_slug': self.project.slug,
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_period/list.html',
            u'changes/sponsorshipperiod_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_SponsorshipPeriodCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsorshipperiod-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_period/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_SponsorshipPeriodCreateView_no_login(self):

        response = self.client.get(reverse('sponsorshipperiod-create', kwargs={
            'project_slug': self.project.slug,
        }))
        self.assertEqual(response.status_code, 302)

    def test_SponsorshipPeriodCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'sponsor': self.sponsor.id,
            'sponsorshiplevel': self.sponsorship_level.id,
            'author': self.user.id
        }
        response = self.client.post(reverse('sponsorshipperiod-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 200)

    def test_SponsorshipPeriodCreate_no_login(self):

        post_data = {
            'sponsor': self.sponsor.id,
            'sponsorship_level': self.sponsorship_level.id
        }
        response = self.client.post(reverse('sponsorshipperiod-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_SponsorshipPeriodUpdateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsorshipperiod-update', kwargs={
            'slug': self.sponsorship_period.slug,
            'project_slug': self.project.slug

        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_period/update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_SponsorshipPeriodUpdateView_no_login(self):

        response = self.client.get(reverse('sponsorshipperiod-update', kwargs={
            'slug': self.sponsorship_period.slug,
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_SponsorshipPeriodUpdate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'sponsor': self.sponsor.id,
            'sponsorshiplevel': self.sponsorship_level.id,
            'author': self.user.id
        }
        response = self.client.post(reverse('sponsorshipperiod-update', kwargs={
            'project_slug': self.project.slug,
            'slug': self.sponsorship_period.slug
        }), post_data)
        self.assertEqual(response.status_code, 200)

    def test_SponsorshipPeriodUpdate_no_login(self):

        post_data = {
            'sponsor': self.sponsor.id,
            'sponsorshiplevel': self.sponsorship_level.id
        }
        response = self.client.post(reverse('sponsorshipperiod-update', kwargs={
            'slug': self.sponsorship_period.slug,
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_SponsorshipPeriodDeleteView_no_login(self):

        response = self.client.get(reverse('sponsorshipperiod-delete', kwargs={
            'project_slug': self.project.slug,
            'slug': self.sponsorship_period.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_SponsorshipPeriodDelete_no_login(self):

        response = self.client.post(reverse('sponsorshipperiod-delete', kwargs={
            'project_slug': self.project.slug,
            'slug': self.sponsorship_period.slug
        }))
        self.assertEqual(response.status_code, 302)
