import json

from django.test import TestCase, override_settings, Client
from django.urls import reverse

from core.model_factories import UserF
from base.tests.model_factories import ProjectF
from lesson.tests.model_factories import (FurtherReadingF,
                                          SectionF,
                                          WorksheetF)


class TestFurtherReadingInvalidLink(TestCase):
    """Test that Futher Reading Invalid Link related view works."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        self.client = Client()
        self.client.post(
            '/set_language/',
            data={'language': 'en'}
        )
        self.user = UserF.create(
            **{'username': 'sumsum', 'is_staff': True})
        self.user.set_password('password')
        self.user.save()

        # Create project
        self.test_project = ProjectF.create(
            name='Test Project'
        )

        # Create section
        self.test_section = SectionF.create(project=self.test_project)
        self.test_worksheet = WorksheetF.create(section=self.test_section,
                                                published=True)
        self.kwargs_project = {'project_slug': self.test_section.project.slug}
        self.kwargs_section = {'slug': self.test_section.slug}
        self.kwargs_section_full = {
            'project_slug': self.test_section.project.slug,
            'slug': self.test_section.slug
        }
        self.kwargs_worksheet_full = {
            'project_slug': self.test_section.project.slug,
            'section_slug': self.test_section.slug,
            'pk': self.test_worksheet.pk
        }
        self.test_further_reading = FurtherReadingF.create(
            worksheet=self.test_worksheet)

        self.test_further_reading.text = (
            'Test for link: <a href="https://changelog.kartoza.com/en/">'
            'https://changelog.kartoza.com/en/</a> and '
            '<a href="https://changelog.qgis.org/should-error">link</a>. '
            'But this one won\'t included')
        self.test_further_reading.save()
        self.client.login(username='sumsum', password='password')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_invalid_FurtherReading_links(self):
        response = self.client.get(
            reverse('further-reading-links', kwargs=self.kwargs_project))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)['data']
        self.assertEqual(
            data[0]['further_reading_url'],
            'https://changelog.kartoza.com/en/'
        )
        self.assertEqual(
            data[1]['further_reading_url'],
            'https://changelog.qgis.org/should-error'
        )
        self.assertEqual(
            data[0]['worksheet'],
            'Test module 0'
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_is_url_exist(self):
        url = reverse('is_url_exist', kwargs=self.kwargs_project)
        url_exist = 'https://changelog.kartoza.com/en/'
        url_not_exist = 'https://should-error.not-exist.must.be/'
        response = self.client.get(url + '?url_string=' + url_exist)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['is_url_exist'], True)
        response = self.client.get(url + '?url_string=' + url_not_exist)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['is_url_exist'], False)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_print_invalid_FurterReading_links(self):
        url = reverse('print_invalid-further-reading-links',
                      kwargs=self.kwargs_project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "filename='Invalid_FurtherReading_test-project.pdf'",
            response.get('Content-Disposition')
        )
