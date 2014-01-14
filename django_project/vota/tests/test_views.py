# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from base.tests.model_factories import ProjectF
from vota.tests.model_factories import VoteF, CommitteeF, BallotF
from core.model_factories import UserF
import logging
import json
import datetime


class TestVoteViews(TestCase):
    """Tests that Vote views work."""

    def setUp(self):
        """
        Setup before each test
        """
        logging.disable(logging.CRITICAL)
        self.myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.myProject = ProjectF.create()
        self.myCommittee = CommitteeF.create(project=self.myProject,
                                             users=[self.myUser])
        self.myBallot = BallotF.create(committee=self.myCommittee)
        self.myVote = VoteF.create(ballot=self.myBallot)

    def test_VoteCreateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('vote-create', kwargs={
            'project_slug': self.myProject.slug,
            'committee_slug': self.myCommittee.slug,
            'ballot_slug': self.myBallot.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'vote/create.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_VoteCreateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('vote-create', kwargs={
            'project_slug': self.myProject.slug,
            'committee_slug': self.myCommittee.slug,
            'ballot_slug': self.myBallot.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_VoteCreate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'choice': 'n'
        }
        myResp = myClient.post(reverse('vote-create', kwargs={
            'project_slug': self.myProject.slug,
            'committee_slug': self.myCommittee.slug,
            'ballot_slug': self.myBallot.slug
        }), postData)
        jsonReturn = myResp.content
        data = json.loads(jsonReturn)
        self.assertTrue(data['successful'])

    def test_VoteCreate_nologin(self):
        myClient = Client()
        postData = {
            'positive': True,
            'abstain': False,
            'negative': False
        }
        myResp = myClient.post(reverse('vote-create', kwargs={
            'project_slug': self.myProject.slug,
            'committee_slug': self.myCommittee.slug,
            'ballot_slug': self.myBallot.slug
        }), postData)
        self.assertEqual(myResp.status_code, 302)


class TestBallotViews(TestCase):
    """Tests that Ballot views work."""

    def setUp(self):
        """
        Setup before each test
        """
        logging.disable(logging.CRITICAL)
        self.myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.myProject = ProjectF.create()
        self.myCommittee = CommitteeF.create(project=self.myProject,
                                             users=[self.myUser])
        self.myBallot = BallotF.create(committee=self.myCommittee)

    def test_BallotDetailView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('ballot-detail', kwargs={
            'project_slug': self.myProject.slug,
            'committee_slug': self.myCommittee.slug,
            'slug': self.myCommittee.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_BallotDetailView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('ballot-detail', kwargs={
            'project_slug': self.myProject.slug,
            'committee_slug': self.myCommittee.slug,
            'slug': self.myBallot.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'ballot/detail.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)
        self.assertEqual(myResp.context_data['ballot'],
                         self.myBallot)

    def test_BallotCreateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('ballot-create'))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'ballot/create.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_BallotCreateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('ballot-create'))
        self.assertEqual(myResp.status_code, 302)

    def test_BallotCreate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'committee': self.myCommittee.id,
            'name': u'New Test Ballot',
            'summary': u'New test summary',
            'description': u'New test description',
            'open_from': datetime.datetime.now() - datetime.timedelta(days=7),
            'closes': datetime.datetime.now() + datetime.timedelta(days=7),
            'private': True,
            'proposer': self.myUser.id
        }
        myResp = myClient.post(reverse('ballot-create'), postData)
        self.assertRedirects(myResp, reverse('ballot-detail', kwargs={
            'project_slug': self.myProject.slug,
            'committee_slug': self.myCommittee.slug,
            'slug': 'new-test-ballot'
        }), status_code=302)

    def test_BallotCreate_nologin(self):
        myClient = Client()
        postData = {
            'positive': True,
            'abstain': False,
            'negative': False
        }
        myResp = myClient.post(reverse('ballot-create'), postData)
        self.assertEqual(myResp.status_code, 302)

    def test_BallotDeleteView_withlogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('ballot-delete', kwargs={
            'slug': self.myBallot.slug,
            'committee_slug': self.myBallot.committee.slug,
            'project_slug': self.myBallot.committee.project.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'ballot/delete.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_BallotDeleteView_nologin(self):
        myClient = Client()
        myResp = myClient.get(reverse('ballot-delete', kwargs={
            'slug': self.myBallot.slug,
            'committee_slug': self.myBallot.committee.slug,
            'project_slug': self.myBallot.committee.project.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_BallotDelete_withLogin(self):
        myClient = Client()
        ballotToDelete = BallotF.create(committee=self.myCommittee)
        myClient.login(username='timlinux', password='password')
        myResp = myClient.post(reverse('ballot-delete', kwargs={
            'slug': ballotToDelete.slug,
            'committee_slug': ballotToDelete.committee.slug,
            'project_slug': ballotToDelete.committee.project.slug
        }), {})
        self.assertRedirects(myResp, reverse('committee-detail', kwargs={
            'slug': self.myCommittee.slug,
            'project_slug': self.myProject.slug
        }), status_code=302)
        #TODO: The following line to test that the object is deleted does not
        #currently pass as expected.
        #self.assertTrue(categoryToDelete.pk is None)

    def test_BallotDelete_noLogin(self):
        myClient = Client()
        ballotToDelete = BallotF.create(committee=self.myCommittee)
        myResp = myClient.post(reverse('ballot-delete', kwargs={
            'slug': ballotToDelete.slug,
            'committee_slug': ballotToDelete.committee.slug,
            'project_slug': self.myCommittee.project.slug
        }))
        self.assertEqual(myResp.status_code, 302)


class TestCommitteeViews(TestCase):
    """Tests that Committee views work."""

    def setUp(self):
        """
        Setup before each test
        """
        logging.disable(logging.CRITICAL)
        self.myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.myProject = ProjectF.create()
        self.myCommittee = CommitteeF.create(project=self.myProject,
                                             users=[self.myUser])

    def test_CommitteeDetailView(self):
        myClient = Client()
        myResp = myClient.get(reverse('committee-detail', kwargs={
            'project_slug': self.myProject.slug,
            'slug': self.myCommittee.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'committee/detail.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)
        self.assertEqual(myResp.context_data['committee'],
                         self.myCommittee)

    def test_CommitteeCreateView_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('committee-create'))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'committee/create.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_CommitteeCreateView_noLogin(self):
        myClient = Client()
        myResp = myClient.get(reverse('committee-create'))
        self.assertEqual(myResp.status_code, 302)

    def test_CommitteeCreate_withLogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        postData = {
            'project': self.myProject.id,
            'name': u'New Test Committee',
            'description': u'New test description',
            'sort_number': 1,
            'quorum_setting': u'50',
            'chair': self.myUser.id,
            'users': [self.myUser.id]
        }
        myResp = myClient.post(reverse('committee-create'), postData)
        self.assertRedirects(myResp, reverse('committee-detail', kwargs={
            'project_slug': self.myProject.slug,
            'slug': 'new-test-committee'
        }), status_code=302)

    def test_CommitteeCreate_nologin(self):
        myClient = Client()
        postData = {
            'positive': True,
            'abstain': False,
            'negative': False
        }
        myResp = myClient.post(reverse('committee-create'), postData)
        self.assertEqual(myResp.status_code, 302)

    def test_CommitteeDeleteView_withlogin(self):
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('committee-delete', kwargs={
            'slug': self.myCommittee.slug,
            'project_slug': self.myCommittee.project.slug
        }))
        self.assertEqual(myResp.status_code, 200)
        expectedTemplates = [
            'committee/delete.html'
        ]
        self.assertEqual(myResp.template_name, expectedTemplates)

    def test_CommitteeDeleteView_nologin(self):
        myClient = Client()
        myResp = myClient.get(reverse('committee-delete', kwargs={
            'slug': self.myCommittee.slug,
            'project_slug': self.myCommittee.project.slug
        }))
        self.assertEqual(myResp.status_code, 302)

    def test_CommitteeDelete_withLogin(self):
        myClient = Client()
        committeeToDelete = CommitteeF.create(project=self.myProject)
        myClient.login(username='timlinux', password='password')
        myResp = myClient.post(reverse('committee-delete', kwargs={
            'slug': committeeToDelete.slug,
            'project_slug': committeeToDelete.project.slug
        }), {})
        self.assertRedirects(myResp, reverse('project-detail', kwargs={
            'slug': self.myProject.slug
        }), status_code=302)
        #TODO: The following line to test that the object is deleted does not
        #currently pass as expected.
        #self.assertTrue(categoryToDelete.pk is None)

    def test_CategoryDelete_noLogin(self):
        myClient = Client()
        committeeToDelete = CommitteeF.create()
        myResp = myClient.post(reverse('category-delete', kwargs={
            'slug': committeeToDelete.slug,
            'project_slug': self.myCommittee.project.slug
        }))
        self.assertEqual(myResp.status_code, 302)
