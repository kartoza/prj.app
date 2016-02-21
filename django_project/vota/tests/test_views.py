# coding=utf-8
# flake8: noqa

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
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.project = ProjectF.create()
        self.committee = CommitteeF.create(project=self.project,
                                             users=[self.user])
        self.ballot = BallotF.create(committee=self.committee)
        self.vote = VoteF.create(ballot=self.ballot)

    def test_VoteCreateView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        resp = client.get(reverse('vote-create', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug,
            'ballot_slug': self.ballot.slug
        }))
        self.assertEqual(resp.status_code, 200)
        expected_templates = [
            'vote/create.html'
        ]
        self.assertEqual(resp.template_name, expected_templates)

    def test_VoteCreateView_no_login(self):
        client = Client()
        response = client.get(reverse('vote-create', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug,
            'ballot_slug': self.ballot.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_VoteCreate_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'choice': 'n'
        }
        response = client.post(reverse('vote-create', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug,
            'ballot_slug': self.ballot.slug
        }), post_data)
        json_return = response.content
        data = json.loads(json_return)
        self.assertTrue(data['successful'])

    def test_VoteCreate_no_login(self):
        client = Client()
        post_data = {
            'positive': True,
            'abstain': False,
            'negative': False
        }
        response = client.post(reverse('vote-create', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug,
            'ballot_slug': self.ballot.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)


class TestBallotViews(TestCase):
    """Tests that Ballot views work."""

    def setUp(self):
        """
        Setup before each test
        """
        logging.disable(logging.CRITICAL)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.project = ProjectF.create()
        self.committee = CommitteeF.create(project=self.project,
                                             users=[self.user])
        self.ballot = BallotF.create(committee=self.committee)

    def test_BallotDetailView_no_login(self):
        client = Client()
        response = client.get(reverse('ballot-detail', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug,
            'slug': self.committee.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_BallotDetailView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('ballot-detail', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug,
            'slug': self.ballot.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'ballot/detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
        self.assertEqual(response.context_data['ballot'],
                         self.ballot)

    def test_BallotListView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('ballot-list', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug
        }))
        self.assertEqual(response.status_code, 200)
        # expected_templates = [
        #     'ballot/list.html',
        # ]
        # self.assertEqual(response.template_name, expected_templates)

    def test_BallotCreateView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('ballot-create', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'ballot/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_BallotCreateView_no_login(self):
        client = Client()
        response = client.get(reverse('ballot-create', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_BallotCreate_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'committee': self.committee.id,
            'name': u'New Test Ballot',
            'summary': u'New test summary',
            'description': u'New test description',
            'open_from': datetime.datetime.now() - datetime.timedelta(days=7),
            'closes': datetime.datetime.now() + datetime.timedelta(days=7),
            'private': True,
            'proposer': self.user.id
        }
        response = client.post(reverse('ballot-create', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug
        }), post_data)
        self.assertRedirects(response, reverse('ballot-detail', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug,
            'slug': 'new-test-ballot'
        }))

    def test_BallotCreate_no_login(self):
        client = Client()
        post_data = {
            'committee': self.committee.id,
            'name': u'New Test Ballot No Login',
            'summary': u'New test summary',
            'description': u'New test description',
            'open_from': datetime.datetime.now() - datetime.timedelta(days=7),
            'closes': datetime.datetime.now() + datetime.timedelta(days=7),
            'private': True,
            'proposer': self.user.id
        }
        response = client.post(reverse('ballot-create', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_BallotUpdateView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('ballot-update', kwargs={
            'project_slug': self.ballot.committee.project.slug,
            'committee_slug': self.ballot.committee.slug,
            'slug': self.ballot.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'ballot/update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_BallotUpdateView_no_login(self):
        client = Client()
        response = client.get(reverse('ballot-update', kwargs={
            'project_slug': self.ballot.committee.project.slug,
            'committee_slug': self.ballot.committee.slug,
            'slug': self.ballot.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_BallotUpdate_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'committee': self.committee.id,
            'name': u'New Test Ballot Update',
            'summary': u'New test summary',
            'description': u'New test description',
            'open_from': datetime.datetime.now() - datetime.timedelta(days=7),
            'closes': datetime.datetime.now() + datetime.timedelta(days=7),
            'private': True,
            'proposer': self.user.id
        }
        response = client.post(reverse('ballot-update', kwargs={
            'project_slug': self.ballot.committee.project.slug,
            'committee_slug': self.ballot.committee.slug,
            'slug': self.ballot.slug
        }), post_data)
        self.assertRedirects(response, reverse('ballot-detail', kwargs={
            'project_slug': self.project.slug,
            'committee_slug': self.committee.slug,
            'slug': self.ballot.slug
        }))

    def test_BallotUpdate_no_login(self):
        client = Client()
        post_data = {
            'committee': self.committee.id,
            'name': u'New Test Ballot Updated',
            'summary': u'New test summary',
            'description': u'New test description',
            'open_from': datetime.datetime.now() - datetime.timedelta(days=7),
            'closes': datetime.datetime.now() + datetime.timedelta(days=7),
            'private': True,
            'proposer': self.user.id
        }
        response = client.post(reverse('ballot-update', kwargs={
            'project_slug': self.ballot.committee.project.slug,
            'committee_slug': self.ballot.committee.slug,
            'slug': self.ballot.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_BallotDeleteView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('ballot-delete', kwargs={
            'slug': self.ballot.slug,
            'committee_slug': self.ballot.committee.slug,
            'project_slug': self.ballot.committee.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'ballot/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_BallotDeleteView_no_login(self):
        client = Client()
        response = client.get(reverse('ballot-delete', kwargs={
            'slug': self.ballot.slug,
            'committee_slug': self.ballot.committee.slug,
            'project_slug': self.ballot.committee.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_BallotDelete_with_login(self):
        client = Client()
        ballot_to_delete = BallotF.create(committee=self.committee)
        client.login(username='timlinux', password='password')
        response = client.post(reverse('ballot-delete', kwargs={
            'slug': ballot_to_delete.slug,
            'committee_slug': ballot_to_delete.committee.slug,
            'project_slug': ballot_to_delete.committee.project.slug
        }), {})
        self.assertRedirects(response, reverse('committee-detail', kwargs={
            'slug': self.committee.slug,
            'project_slug': self.project.slug
        }))

        # TODO: The following line to test that
        # the object is deleted does not currently pass as expected.
        # self.assertTrue(category_to_delete.pk is None)

    def test_BallotDelete_no_login(self):
        client = Client()
        ballot_to_delete = BallotF.create(committee=self.committee)
        response = client.post(reverse('ballot-delete', kwargs={
            'slug': ballot_to_delete.slug,
            'committee_slug': ballot_to_delete.committee.slug,
            'project_slug': self.committee.project.slug
        }))
        self.assertEqual(response.status_code, 302)


class TestCommitteeViews(TestCase):
    """Tests that Committee views work."""

    def setUp(self):
        """
        Setup before each test
        """
        logging.disable(logging.CRITICAL)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.project = ProjectF.create()
        self.committee = CommitteeF.create(project=self.project,
                                             users=[self.user])

    def test_CommitteeDetailView(self):
        client = Client()
        response = client.get(reverse('committee-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': self.committee.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'committee/detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
        self.assertEqual(response.context_data['committee'],
                         self.committee)

    def test_CommitteeCreateView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('committee-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'committee/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CommitteeCreateView_no_login(self):
        client = Client()
        response = client.get(reverse('committee-create', kwargs={
            'project_slug': self.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_CommitteeCreate_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'project': self.project.id,
            'name': u'New Test Committee',
            'description': u'New test description',
            'sort_number': 1,
            'quorum_setting': u'50',
            'chair': self.user.id,
            'users': [self.user.id]
        }
        response = client.post(reverse('committee-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertRedirects(response, reverse('committee-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': 'new-test-committee'
        }))

    def test_CommitteeCreate_no_login(self):
        client = Client()
        post_data = {
            'positive': True,
            'abstain': False,
            'negative': False
        }
        response = client.post(reverse('committee-create', kwargs={
            'project_slug': self.project.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_CommitteeUpdateView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('committee-update', kwargs={
            'project_slug': self.committee.project.slug,
            'slug': self.committee.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'committee/update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CommitteeUpdateView_no_login(self):
        client = Client()
        response = client.get(reverse('committee-update', kwargs={
            'project_slug': self.committee.project.slug,
            'slug': self.committee.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_CommitteeUpdate_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        post_data = {
            'project': self.project.id,
            'name': u'New Test Committee Updated',
            'description': u'New test description',
            'sort_number': 1,
            'quorum_setting': u'100',
            'chair': self.user.id,
            'users': [self.user.id]
        }
        response = client.post(reverse('committee-update', kwargs={
            'project_slug': self.committee.project.slug,
            'slug': self.committee.slug
        }), post_data)
        self.assertRedirects(response, reverse('committee-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': self.committee.slug
        }))

    def test_CommitteeUpdate_no_login(self):
        client = Client()
        post_data = {
            'project': self.project.id,
            'name': u'New Test Committee',
            'description': u'New test description',
            'sort_number': 1,
            'quorum_setting': u'50',
            'chair': self.user.id,
            'users': [self.user.id]
        }
        response = client.post(reverse('committee-update', kwargs={
            'project_slug': self.committee.project.slug,
            'slug': self.committee.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

    def test_CommitteeDeleteView_with_login(self):
        client = Client()
        client.login(username='timlinux', password='password')
        response = client.get(reverse('committee-delete', kwargs={
            'slug': self.committee.slug,
            'project_slug': self.committee.project.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'committee/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CommitteeDeleteView_no_login(self):
        client = Client()
        response = client.get(reverse('committee-delete', kwargs={
            'slug': self.committee.slug,
            'project_slug': self.committee.project.slug
        }))
        self.assertEqual(response.status_code, 302)

    def test_CommitteeDelete_with_login(self):
        client = Client()
        committee_to_delete = CommitteeF.create(project=self.project)
        client.login(username='timlinux', password='password')
        response = client.post(reverse('committee-delete', kwargs={
            'slug': committee_to_delete.slug,
            'project_slug': committee_to_delete.project.slug
        }), {})
        self.assertRedirects(response, reverse('project-detail', kwargs={
            'slug': self.project.slug
        }))
        # TODO: The following line to test that the object is deleted does not currently pass as expected.
        # self.assertTrue(category_to_delete.pk is None)

    def test_CategoryDelete_no_login(self):
        client = Client()
        committee_to_delete = CommitteeF.create()
        response = client.post(reverse('category-delete', kwargs={
            'slug': committee_to_delete.slug,
            'project_slug': self.committee.project.slug
        }))
        self.assertEqual(response.status_code, 302)
