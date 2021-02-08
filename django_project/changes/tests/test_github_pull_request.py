""" Tests about the GitHub harvesting. """

import unittest
import logging

from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse

from base.tests.model_factories import ProjectF
from changes.utils.github_pull_request import parse_funded_by
from changes.tests.model_factories import (
    CategoryF,
    EntryF,
    VersionF)
from core.model_factories import UserF


class TestGithubPullRequest(unittest.TestCase):

    def test_funded_by(self):
        """ Test to parse the PR content and find the funded by. """
        # Normal, with my name in capital letters, HTTP
        body = (
            'This is a new feature\n'
            'Funded by I\'am AWESOME http://myself.me'
        )
        content, funded_by, url = parse_funded_by(body)
        self.assertEqual('This is a new feature', content)
        self.assertEqual('I\'am AWESOME', funded_by)
        self.assertEqual('http://myself.me', url)

        # In the middle of the PR content, no URL
        body = (
            'This \n'
            'is a new feature\n'
            'Funded by myself.inc\n'
            'It will rock !'
        )
        content, funded_by, url = parse_funded_by(body)
        self.assertEqual('This \nis a new feature\nIt will rock !', content)
        self.assertEqual('myself.inc', funded_by)
        self.assertEqual('', url)

        # No funded by
        body = (
            'This \n'
            'is a new feature\n'
            'It will rock !'
        )
        content, funded_by, url = parse_funded_by(body)
        self.assertEqual('This \nis a new feature\nIt will rock !', content)
        self.assertEqual('', funded_by)
        self.assertEqual('', url)

        # With spaces/tab and upper/lower case, HTTPS
        body = (
            'This is a new feature\n'
            '   funded BY   myself.inc  https://myself.me'
        )
        content, funded_by, url = parse_funded_by(body)
        self.assertEqual('This is a new feature', content)
        self.assertEqual('myself.inc', funded_by)
        self.assertEqual('https://myself.me', url)

        # With markdown and two \n
        body = (
            'This is a new feature :\n\n'
            '* Funded by myself.inc https://myself.me\n'
            '* IT\n'
            '* WILL\n'
            '* ROCK'
        )
        content, funded_by, url = parse_funded_by(body)
        self.assertEqual(
            'This is a new feature :\n\n* IT\n* WILL\n* ROCK', content)
        self.assertEqual('myself.inc', funded_by)
        self.assertEqual('https://myself.me', url)

        # No name, only URL
        body = (
            'This is a new feature :\n'
            '* Funded by https://myself.me\n'
        )
        content, funded_by, url = parse_funded_by(body)
        self.assertEqual('This is a new feature :\n', content)
        self.assertEqual('', funded_by)
        self.assertEqual('https://myself.me', url)

        # No name, no URL, but with "funded by"
        body = (
            'This is a new feature :\n'
            '* Funded by\n'
            '* Another line'
        )
        content, funded_by, url = parse_funded_by(body)
        self.assertEqual('This is a new feature :\n* Another line', content)
        self.assertEqual('', funded_by)
        self.assertEqual('', url)


class TestGithubDownloadImage(TestCase):
    """Tests that Category views work."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
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
            title='testentry')
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.user.set_password('password')
        self.user.save()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.version.delete()
        self.category.delete()
        self.user.delete()
        self.entry.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_download_all_referenced_images(self):
        self.entry.description = (
            '![image](https://user-images.githubusercontent.com/40058076/'
            '106831321-a99d0900-66ca-11eb-8764-11627dcfbf17.png)   and '
            '![image](https://user-images.githubusercontent.com/40058076/'
            '106831433-dea95b80-66ca-11eb-8026-6823084d726e.png)'
        )
        self.entry.save()
        self.client.login(username='timlinux', password='password')
        response = self.client.get(
            reverse('download-referenced-images', kwargs={
                'slug': self.version.slug,
                'project_slug': self.project.slug
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'success'}
        )
        self.assertFalse('/media/media' in self.entry.image_file.url)
        self.assertTrue('/media/images/entries' in self.entry.image_file.url)
