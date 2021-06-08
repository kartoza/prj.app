""" Tests about the GitHub harvesting. """

import unittest
import logging
import re

from unittest import mock

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

from changes.views import create_entry_from_github_pr
from changes.models import Entry


def mocked_request_get_github(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://api.github.com/users/qgis':
        return MockResponse({
            'html_url': 'https://github.com/qgis',
            'name': 'name'
        }, 200)

    return MockResponse(None, 404)


class TestGithubPullRequest(unittest.TestCase):

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        self.project = ProjectF.create()
        self.category = CategoryF.create(project=self.project)
        self.version = VersionF.create(project=self.project)
        self.user = UserF.create(**{
            'username': 'suman',
            'password': 'password',
            'is_staff': True
        })
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        self.project.delete()
        self.version.delete()
        self.category.delete()
        self.user.delete()

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

        # Switch to "sponsored by", with markdown and capital letters,
        body = (
            'This is a new feature :\n\n'
            '* SPONSORED BY myself.inc https://myself.me\n'
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
        self.assertEqual('This is a new feature :', content)
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

        # With a separator and spaces, accents, this is
        body = (
            'This is a new feature.\n'
            'THis is sponsored by : MÉTRôpole dé @LYÖN'
        )
        content, funded_by, url = parse_funded_by(body)
        self.assertEqual('This is a new feature.', content)
        self.assertEqual('MÉTRôpole dé @LYÖN', funded_by)
        self.assertEqual('', url)

        # With a separator, no spaces, this is
        body = (
            'This is a new feature.\n'
            'This is sponsored by:Lyon\n'
        )
        content, funded_by, url = parse_funded_by(body)
        self.assertEqual('This is a new feature.', content)
        self.assertEqual('Lyon', funded_by)
        self.assertEqual('', url)

    @override_settings(VALID_DOMAIN=['testserver', ])
    @mock.patch('requests.get', side_effect=mocked_request_get_github)
    def test_create_entry_from_github_pr_timeout(self, mock_request):
        RESULT_RESPONSE_GITHUB = [
            {
                'name': 'name',
                'body': '## Description\r\n',
                'html_url': 'https://github.com/kartoza/prj.app/issues/1309',
                'repository_url':
                    'https://api.github.com/repos/qgis/QGIS-Django',
                'title': 'Reorder expression operators',
                'updated_at': '2021-02-21T22:45:33Z',
                'url': 'https://api.github.com/repos/qgis/QGIS/issues/41692',
                'user': {
                    'html_url': 'https://github.com/qgis',
                    'url': 'https://api.github.com/users/qgis'
                }
            }
        ]

        create_entry_from_github_pr(
            self.version,
            self.category,
            RESULT_RESPONSE_GITHUB,
            self.user
        )

        self.entry_created = Entry.objects.filter(author=self.user).all()
        self.assertEqual(len(self.entry_created), 1)
        self.assertEqual(
            self.entry_created[0].developer_url, 'https://github.com/qgis')


class TestGithubDownloadImage(TestCase):
    """Tests that Category views work."""

    @classmethod
    def setUpTestData(cls):
        cls.Entry = EntryF._meta.model

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
            '106831433-dea95b80-66ca-11eb-8026-6823084d726e.png)'
            ' this should be in description '
            '![image](https://user-images.githubusercontent.com/40058076/'
            '106831321-a99d0900-66ca-11eb-8764-11627dcfbf17.png)'
        )
        self.entry.image_file = None
        self.entry.save()
        # Ensure the image_file is None
        self.assertFalse(self.entry.image_file)
        self.client.login(username='timlinux', password='password')
        response = self.client.get(
            reverse('download-referenced-images', kwargs={
                'slug': self.version.slug,
                'project_slug': self.project.slug
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        entry = self.Entry.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'success'}
        )
        self.assertTrue(entry.image_file)

        #  check if image removed from description
        rgx = ('<img.*?https://user-images.githubusercontent.com/40058076/'
               '106831433-dea95b80-66ca-11eb-8026-6823084d726e.png.*?/>')
        is_match = re.match(rgx, entry.description)
        self.assertIsNone(
            is_match,
            msg=f'image regex pattern {rgx} must be not in description '
                f'{entry.description}'
        )

        # check if another image is in description
        self.assertIn(
            ('/media/images/entries/106831321-a99d0900-66ca-11eb-8764-'
             '11627dcfbf17'),
            entry.description
        )

        # chek if text is in description
        self.assertIn('this should be in description', entry.description)
