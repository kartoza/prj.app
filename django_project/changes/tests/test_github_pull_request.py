""" Tests about the GitHub harvesting. """

import unittest

from changes.utils.github_pull_request import parse_funded_by


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
