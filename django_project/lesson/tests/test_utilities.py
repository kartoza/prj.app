# coding=utf-8
"""Test for lesson utilities."""

from django.test import TestCase

from lesson.tests.model_factories import (FurtherReadingF,
                                          SectionF,
                                          WorksheetF)
from base.tests.model_factories import ProjectF

from lesson.utilities import GetInvalidFurtherReadingLink


def side_effect_build_absolute_uri(value):
    """Mocking build_absolute_uri side_effect.

    Return the value which is the relative path instead of absolute path
    """
    return value


class InvalidFurtherReadingURL(TestCase):

    def setUp(self):
        # Create project
        self.test_project = ProjectF.create()

        # Create section
        self.test_section = SectionF.create(
            project=self.test_project)
        self.test_worksheet = WorksheetF.create(
            section=self.test_section,
            published=True,
            module='Test Invalid Link'
        )
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

    def test_get_further_reading_link_list(self):
        self.test_further_reading.text = (
            'Test for link: https://changelog.kartoza.com/en/ '
            'and '
            'https://changelog.qgis.org/en/qgis/lessons/#introduction-qgis-1')
        self.test_further_reading.save()
        obj = GetInvalidFurtherReadingLink(self.test_project)
        result = obj.get_url_list(self.test_further_reading.text)
        self.assertEqual(
            result,
            ['https://changelog.kartoza.com/en/',
             'https://changelog.qgis.org/en/qgis/lessons/#introduction-qgis-1']
        )

    def test_check_if_url_invalid_return_none(self):
        url = 'http://www.example.com'
        obj = GetInvalidFurtherReadingLink(self.test_project)
        result = obj.check_if_url_invalid(url)
        self.assertFalse(result)

    def test_check_if_url_invalid_return_not_none(self):
        obj = GetInvalidFurtherReadingLink(self.test_project)
        url = 'http://www .example.com'
        result = obj.check_if_url_invalid(url)
        self.assertTrue(result)
        self.assertEqual(result, url)
        url = 'http://www.example.com/this-page-is-not-exist/'
        result = obj.check_if_url_invalid(url)
        self.assertTrue(result)
        self.assertEqual(result, url)

    def test_get_all_invalid_url(self):
        self.test_further_reading.text = (
            'Test for invalid link: '
            'http://www.example.com/this-page-is-not-exist/')
        self.test_further_reading.save()
        obj = GetInvalidFurtherReadingLink(self.test_project)
        result = obj.get_all_invalid_url()
        worksheet_url = obj.get_worksheet_url(
            self.test_worksheet.pk,
            self.test_worksheet.section.slug,
            self.test_worksheet.section.project.slug
        )
        self.assertEqual(
            result,
            ([f'<a href="{worksheet_url}">{self.test_worksheet}</a> '
              f'has invalid links or unavailable links: '
              f'http://www.example.com/this-page-is-not-exist/']),
            msg=f'{result}')
