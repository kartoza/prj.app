# coding=utf-8
import logging
from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse
from certification.tests.model_factories import (
    ProjectF,
    UserF,
    CertifyingOrganisationF,
    CourseF
)


class TestCourseView(TestCase):
    """Test that Course View works."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """
        Setup before each test
        We force the locale to en otherwise it will use
        the locale of the host running the tests and we
        will get unpredictable results / 404s
        """

        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.user = UserF.create(**{
            'username': 'anita',
            'password': 'password',
            'is_staff': True
        })
        self.user.set_password('password')
        self.user.save()
        self.project = ProjectF.create()
        self.certifying_organisation = CertifyingOrganisationF.create(
            project=self.project
        )
        self.course = CourseF.create(
            certifying_organisation=self.certifying_organisation
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """

        self.course.delete()
        self.certifying_organisation.delete()
        self.project.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_detail_view(self):
        client = Client()
        response = client.get(reverse('course-detail', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': self.course.slug
        }))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_detail_with_duplicates(self):
        self.client.login(username='anita', password='password')
        course2 = CourseF.create(
            certifying_organisation=self.certifying_organisation
        )
        course2.slug = self.course.slug
        course2.save()

        response = self.client.get(reverse('course-detail', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': course2.slug
        }))
        self.assertEqual(response.status_code, 302)

        expected_url = reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': self.certifying_organisation.slug,
        })
        self.assertRedirects(response, expected_url)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_detail_view_object_does_not_exist(self):
        client = Client()
        response = client.get(reverse('course-detail', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': 'random',
            'slug': self.course.slug
        }))
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('course-detail', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': 'random'
        }))
        self.assertEqual(response.status_code, 404)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_view(self):
        self.client.login(username='anita', password='password')
        post_data = {
            'name': 'new name',
            'language': 'Japanese',
        }
        response = self.client.post(
            reverse('course-update', kwargs={
                'project_slug': self.project.slug,
                'organisation_slug': self.certifying_organisation.slug,
                'slug': self.course.slug
            }), post_data)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_with_duplicates(self):
        self.client.login(username='anita', password='password')
        course2 = CourseF.create(
            certifying_organisation=self.certifying_organisation
        )
        course2.slug = self.course.slug
        course2.save()
        post_data = {
            'name': 'new course name',
            'language': 'Indonesian',
        }
        response = self.client.get(reverse('course-update', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': course2.slug
        }), post_data)
        self.assertEqual(response.status_code, 302)

        expected_url = reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': self.certifying_organisation.slug,
        })
        self.assertRedirects(response, expected_url)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_delete_with_duplicates(self):
        self.client.login(username='anita', password='password')
        course2 = CourseF.create(
            certifying_organisation=self.certifying_organisation
        )
        course2.slug = self.course.slug
        course2.save()
        response = self.client.get(reverse('course-delete', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': course2.slug
        }))
        self.assertEqual(response.status_code, 302)
        expected_url = reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': self.certifying_organisation.slug,
        })
        self.assertRedirects(response, expected_url)
