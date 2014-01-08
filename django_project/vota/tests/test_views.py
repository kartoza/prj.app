# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from base.tests.model_factories import ProjectF
from vota.tests.model_factories import VoteF, CommitteeF, BallotF
from core.model_factories import UserF
import logging
import json


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
            'positive': True,
            'abstain': False,
            'negative': False
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


