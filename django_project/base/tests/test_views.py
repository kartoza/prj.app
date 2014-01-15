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
        self.myTestProject = ProjectF.create()
        self.myUnapprovedProject = ProjectF.create(approved=False)
        self.myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

    def test_ProjectListView(self):
        myClient = Client()
        myResp = myClient.get(reverse('home'))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'project/list.html', u'base/project_list.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)
        self.assertEqual(myResp.context_data['object_list'][0],
                         self.myTestProject)

    def test_ProjectCreateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('project-create'))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'project/create.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_ProjectCreateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('project-create'))
        self.assertEqual(myResp.status_code, 302)

    def test_ProjectCreate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'name': u'New Test Project',
            'owner': self.myUser.id
        }
        myResp = myClient.post(reverse('project-create'), postData)
        self.assertRedirects(myResp, reverse('pending-project-list'),
                             status_code=302)

    def test_ProjectCreate_nologin(self):
        myClient = Client()
        postData = {
            'name': u'New Test Project'
        }
        myResp = myClient.post(reverse('project-create'), postData)
        self.assertEqual(myResp.status_code, 302)

    def test_ProjectUpdateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('project-update', kwargs={
            'slug': self.myTestProject.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'project/update.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_ProjectUpdateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('project-update', kwargs={
            'slug': self.myTestProject.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_ProjectUpdate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'name': u'New Test Project Updated',
            'owner': self.myUser.id
        }
        myResp = myClient.post(reverse('project-update', kwargs={
            'slug': self.myTestProject.slug
        }), postData)
        self.assertRedirects(myResp, reverse('project-detail', kwargs={
            'slug': self.myTestProject.slug
        }), status_code=302)

    def test_ProjectUpdate_nologin(self):
        myClient = Client()
        postData = {
            'name': u'New Test Project Updated',
            'owner': self.myUser.id
        }
        myResp = myClient.post(reverse('project-update', kwargs={
            'slug': self.myTestProject.slug
        }), postData)
        self.assertEqual(myResp.status_code, 302)

    def test_ProjectDetailView(self):
        myClient = Client()
        myResp = myClient.get(reverse('project-detail', kwargs={
            'slug': self.myTestProject.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'project/detail.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_ProjectDeleteView_withlogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('project-delete', kwargs={
            'slug': self.myTestProject.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'project/delete.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_ProjectDeleteView_nologin(self):
        myClient = Client()
        myResp = myClient.get(reverse('project-delete', kwargs={
            'slug': self.myTestProject.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_ProjectDelete_withLogin(self):
        myClient = Client()
        projectToDelete = ProjectF.create()
        postData = {
            'pk': projectToDelete.pk
        }
        myClient.login(username='timlinux', password='password')
        myResp = myClient.post(reverse('project-delete', kwargs={
            'slug': projectToDelete.slug
        }), postData)
        self.assertRedirects(myResp, reverse('project-list'),
                             status_code=302)
        #TODO: The following line to test that the object is deleted does not
        #currently pass as expected.
        #self.assertTrue(projectToDelete.pk is None)

    def test_ProjectDelete_noLogin(self):
        myClient = Client()
        projectToDelete = ProjectF.create()
        myResp = myClient.post(reverse('project-delete', kwargs={
            'slug': projectToDelete.slug
        }))
        self.assertEqual(myResp.status_code, 302)
