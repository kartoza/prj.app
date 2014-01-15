# coding=utf-8
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
        self.myProject = ProjectF.create()
        self.myCategory = CategoryF.create(project=self.myProject)
        self.myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def test_CategoryListView(self):
        myClient = Client()
        myResp = myClient.get(reverse('category-list', kwargs={
            'project_slug': self.myProject.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'category/list.html', u'changes/category_list.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)
        self.assertEqual(myResp.context_data['object_list'][0],
                         self.myCategory)

    def test_CategoryCreateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('category-create'))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'category/create.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_CategoryCreateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('category-create'))
        self.assertEqual(myResp.status_code, 302)

    def test_CategoryCreate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'name': u'New Test Category',
            'project': self.myProject.id,
            'sort_number': 0
        }
        myResp = myClient.post(reverse('category-create'), postData)
        self.assertRedirects(myResp, reverse('pending-category-list', kwargs={
            'project_slug': self.myProject.slug
        }), status_code=302)

    def test_CategoryCreate_nologin(self):
        myClient = Client()
        postData = {
            'name': u'New Test Category'
        }
        myResp = myClient.post(reverse('category-create'), postData)
        self.assertEqual(myResp.status_code, 302)

    def test_CategoryDetailView(self):
        myClient = Client()
        myResp = myClient.get(reverse('category-detail', kwargs={
            'slug': self.myCategory.slug,
            'project_slug': self.myCategory.project.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'category/detail.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_CategoryDeleteView_withlogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('category-delete', kwargs={
            'slug': self.myCategory.slug,
            'project_slug': self.myCategory.project.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'category/delete.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_CategoryDeleteView_nologin(self):
        myClient = Client()
        myResp = myClient.get(reverse('category-delete', kwargs={
            'slug': self.myCategory.slug,
            'project_slug': self.myCategory.project.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_CategoryDelete_withLogin(self):
        myClient = Client()
        categoryToDelete = CategoryF.create(project=self.myProject)
        myClient.login(username='timlinux', password='password')
        myResp = myClient.post(reverse('category-delete', kwargs={
            'slug': categoryToDelete.slug,
            'project_slug': categoryToDelete.project.slug
        }), {})
        self.assertRedirects(myResp, reverse('category-list', kwargs={
            'project_slug': self.myProject.slug
        }), status_code=302)
        #TODO: The following line to test that the object is deleted does not
        #currently pass as expected.
        #self.assertTrue(categoryToDelete.pk is None)

    def test_CategoryDelete_noLogin(self):
        myClient = Client()
        categoryToDelete = CategoryF.create()
        myResp = myClient.post(reverse('category-delete', kwargs={
            'slug': categoryToDelete.slug,
            'project_slug': self.myCategory.project.slug
        }))
        self.assertEqual(myResp.status_code, 302)


class TestEntryViews(TestCase):
    """Tests that Entry views work."""

    def setUp(self):
        """
        Setup before each test
        """
        logging.disable(logging.CRITICAL)
        self.myProject = ProjectF.create()
        self.myVersion = VersionF.create(project=self.myProject)
        self.myCategory = CategoryF.create(project=self.myProject)
        self.myEntry = EntryF.create(category=self.myCategory,
                                     version=self.myVersion)
        self.myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def test_EntryListView(self):
        myClient = Client()
        myResp = myClient.get(reverse('entry-list', kwargs={
            'project_slug': self.myProject.slug,
            'version_slug': self.myEntry.version.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'entry/list.html', u'changes/entry_list.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)
        self.assertEqual(myResp.context_data['object_list'][0],
                         self.myEntry)

    def test_EntryCreateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('entry-create'))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'entry/create.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_EntryCreateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('entry-create'))
        self.assertEqual(myResp.status_code, 302)

    def test_EntryCreate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'title': u'New Test Entry',
            'version': self.myVersion.id,
            'category': self.myCategory.id,
            'author': self.myUser.id
        }
        myResp = myClient.post(reverse('entry-create'), postData)
        self.assertRedirects(myResp, reverse('pending-entry-list', kwargs={
            'project_slug': self.myProject.slug,
            'version_slug': self.myVersion.slug
        }), status_code=302)

    def test_EntryCreate_noLogin(self):
        myClient = Client()
        postData = {
            'title': u'New Test Entry',
            'version': self.myVersion.id,
            'category': self.myCategory.id
        }
        myResp = myClient.post(reverse('entry-create'), postData)
        self.assertEqual(myResp.status_code, 302)

    def test_EntryUpdateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('entry-update', kwargs={
            'project_slug': self.myEntry.version.project.slug,
            'version_slug': self.myEntry.version.slug,
            'slug': self.myEntry.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'entry/update.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_EntryUpdateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('entry-update', kwargs={
            'project_slug': self.myEntry.version.project.slug,
            'version_slug': self.myEntry.version.slug,
            'slug': self.myEntry.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_EntryUpdate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'title': u'New Test Entry Updated',
            'version': self.myVersion.id,
            'category': self.myCategory.id,
            'author': self.myUser.id
        }
        myResp = myClient.post(reverse('entry-update', kwargs={
            'project_slug': self.myEntry.version.project.slug,
            'version_slug': self.myEntry.version.slug,
            'slug': self.myEntry.slug
        }), postData)
        self.assertRedirects(myResp, reverse('pending-entry-list', kwargs={
            'project_slug': self.myProject.slug,
            'version_slug': self.myVersion.slug
        }), status_code=302)

    def test_EntryUpdate_nologin(self):
        myClient = Client()
        postData = {
            'title': u'New Test Entry Updated',
            'version': self.myVersion.id,
            'category': self.myCategory.id
        }
        myResp = myClient.post(reverse('entry-update', kwargs={
            'project_slug': self.myEntry.version.project.slug,
            'version_slug': self.myEntry.version.slug,
            'slug': self.myEntry.slug
        }), postData)
        self.assertEqual(myResp.status_code, 302)

    def test_EntryDetailView(self):
        myClient = Client()
        myResp = myClient.get(reverse('entry-detail', kwargs={
            'slug': self.myEntry.slug,
            'project_slug': self.myProject.slug,
            'version_slug': self.myVersion.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'entry/detail.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_EntryDeleteView_withlogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('entry-delete', kwargs={
            'slug': self.myEntry.slug,
            'project_slug': self.myProject.slug,
            'version_slug': self.myVersion.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'entry/delete.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_EntryDeleteView_nologin(self):
        myClient = Client()
        myResp = myClient.get(reverse('entry-delete', kwargs={
            'slug': self.myEntry.slug,
            'project_slug': self.myVersion.project.slug,
            'version_slug': self.myVersion.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_EntryDelete_withLogin(self):
        myClient = Client()
        entryToDelete = EntryF.create(category=self.myCategory,
                                      version=self.myVersion)
        myClient.login(username='timlinux', password='password')
        myResp = myClient.post(reverse('entry-delete', kwargs={
            'slug': entryToDelete.slug,
            'project_slug': entryToDelete.version.project.slug,
            'version_slug': self.myVersion.slug
        }), {})
        self.assertRedirects(myResp, reverse('entry-list', kwargs={
            'project_slug': self.myProject.slug,
            'version_slug': self.myVersion.slug
        }), status_code=302)
        #TODO: The following line to test that the object is deleted does not
        #currently pass as expected.
        #self.assertTrue(entryToDelete.pk is None)

    def test_EntryDelete_noLogin(self):
        myClient = Client()
        entryToDelete = EntryF.create(category=self.myCategory,
                                      version=self.myVersion)
        myResp = myClient.post(reverse('entry-delete', kwargs={
            'slug': entryToDelete.slug,
            'project_slug': self.myVersion.project.slug,
            'version_slug': self.myVersion.slug
        }))
        self.assertEqual(myResp.status_code, 302)


class TestVersionViews(TestCase):
    """Tests that Version views work."""

    def setUp(self):
        """
        Setup before each test
        """
        logging.disable(logging.CRITICAL)
        self.myProject = ProjectF.create()
        self.myVersion = VersionF.create(project=self.myProject)
        self.myCategory = CategoryF.create(project=self.myProject)

        self.myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def test_VersionListView(self):
        myClient = Client()
        myResp = myClient.get(reverse('version-list', kwargs={
            'project_slug': self.myProject.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'version/list.html', u'changes/version_list.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)
        self.assertEqual(myResp.context_data['object_list'][0],
                         self.myVersion)

    def test_VersionCreateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('version-create'))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'version/create.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_VersionCreateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('version-create'))
        self.assertEqual(myResp.status_code, 302)

    def test_VersionCreate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'project': self.myProject.id,
            'name': u'New Test Version',
            'description': u'This is a test description',
            'author': self.myUser.id
        }
        myResp = myClient.post(reverse('version-create'), postData)
        self.assertRedirects(myResp, reverse('pending-version-list', kwargs={
            'project_slug': self.myProject.slug
        }), status_code=302)

    def test_VersionCreate_nologin(self):
        myClient = Client()
        postData = {
            'project': self.myProject.id,
            'name': u'New Test Version',
            'description': u'This is a test description'
        }
        myResp = myClient.post(reverse('version-create'), postData)
        self.assertEqual(myResp.status_code, 302)

    def test_VersionUpdateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('version-update', kwargs={
            'project_slug': self.myVersion.project.slug,
            'slug': self.myVersion.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'version/update.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_VersionUpdateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('version-update', kwargs={
            'project_slug': self.myVersion.project.slug,
            'slug': self.myVersion.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_VersionUpdate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'project': self.myProject.id,
            'name': u'New Test Version Updated',
            'description': u'This is a test description',
            'author': self.myUser.id
        }
        myResp = myClient.post(reverse('version-update', kwargs={
            'project_slug': self.myVersion.project.slug,
            'slug': self.myVersion.slug
        }), postData)
        self.assertRedirects(myResp, reverse('version-list', kwargs={
            'project_slug': self.myProject.slug
        }), status_code=302)

    def test_VersionUpdate_nologin(self):
        myClient = Client()
        postData = {
            'project': self.myProject.id,
            'name': u'New Test Version',
            'description': u'This is a test description'
        }
        myResp = myClient.post(reverse('version-update', kwargs={
            'project_slug': self.myVersion.project.slug,
            'slug': self.myVersion.slug
        }), postData)
        self.assertEqual(myResp.status_code, 302)

    def test_VersionDetailView(self):
        myClient = Client()
        myResp = myClient.get(reverse('version-detail', kwargs={
            'slug': self.myVersion.slug,
            'project_slug': self.myProject.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'version/detail.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_VersionDeleteView_withlogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('version-delete', kwargs={
            'slug': self.myVersion.slug,
            'project_slug': self.myProject.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'version/delete.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_VersionDeleteView_nologin(self):
        myClient = Client()
        myResp = myClient.get(reverse('version-delete', kwargs={
            'slug': self.myVersion.slug,
            'project_slug': self.myVersion.project.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_VersionDelete_withLogin(self):
        myClient = Client()
        versionToDelete = VersionF.create(project=self.myProject)
        postData = {
            'pk': versionToDelete.pk
        }
        myClient.login(username='timlinux', password='password')
        myResp = myClient.post(reverse('version-delete', kwargs={
            'slug': versionToDelete.slug,
            'project_slug': versionToDelete.project.slug
        }), postData)
        self.assertRedirects(myResp, reverse('version-list', kwargs={
            'project_slug': self.myProject.slug
        }), status_code=302)
        #TODO: The following line to test that the object is deleted does not
        #currently pass as expected.
        #self.assertTrue(versionToDelete.pk is None)

    def test_VersionDelete_noLogin(self):
        myClient = Client()
        versionToDelete = VersionF.create(project=self.myProject)
        myResp = myClient.post(reverse('version-delete', kwargs={
            'slug': versionToDelete.slug,
            'project_slug': self.myVersion.project.slug
        }))
        self.assertEqual(myResp.status_code, 302)
