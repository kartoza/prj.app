# coding=utf-8
import datetime
import logging
from bs4 import BeautifulSoup as Soup

from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse
from certification.tests.model_factories import (
    ProjectF,
    UserF,
    CertifyingOrganisationF,
    CertificateTypeF,
    ProjectCertificateTypeF,
    CourseF,
    CourseConvenerF, AttendeeF, CertificateF, CourseAttendeeF
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
        self.certificate_type = CertificateTypeF.create()
        self.project_cert_type = ProjectCertificateTypeF.create(
            project=self.project,
            certificate_type=self.certificate_type
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
    def test_create_course_must_showing_CertificateTypes(self):
        self.client.login(username='anita', password='password')
        response = self.client.get(reverse('course-create', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
        }))
        self.assertEqual(response.status_code, 200)
        soup = Soup(response.content, "html5lib")
        cert_type_option = soup.find(
            'select',
            {'id': 'id_certificate_type'}
        ).find_all('option')
        self.assertIn(
            self.certificate_type.name,
            [cert_type.text for cert_type in cert_type_option]
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_detail_view(self):
        client = Client()
        attendee = AttendeeF.create()
        CourseAttendeeF.create(
            attendee=attendee,
            course=self.course
        )
        CertificateF.create(
            attendee=attendee,
            course=self.course,
            issue_date=datetime.datetime.now()
        )

        old_attendee = AttendeeF.create()
        CourseAttendeeF.create(
            attendee=old_attendee,
            course=self.course
        )
        cert = CertificateF.create(
            attendee=old_attendee,
            course=self.course
        )
        cert.issue_date = datetime.datetime.now() - datetime.timedelta(days=7)
        cert.save()

        response = client.get(reverse('course-detail', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': self.course.slug
        }))
        self.assertEqual(response.status_code, 200)
        course_attendees = response.context_data['attendees']
        for course_attendee in course_attendees:
            if course_attendee.attendee_id == attendee.id:
                self.assertTrue(course_attendee.editable)
            else:
                self.assertFalse(course_attendee.editable)

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

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_inactive_convener_should_not_be_in_the_course_convener_list(self):
        convener = UserF.create(**{
            'username': 'convener',
            'password': 'password',
            'first_name': 'Pretty',
            'last_name': 'Smart',
            'is_staff': True
        })
        convener_inactive = UserF.create(**{
            'username': 'inactive_convener',
            'password': 'password',
            'first_name': 'Wonder',
            'last_name': 'Woman',
            'is_staff': True
        })
        CourseConvenerF.create(
            user=convener,
            certifying_organisation=self.certifying_organisation
        )
        CourseConvenerF.create(
            user=convener_inactive,
            certifying_organisation=self.certifying_organisation,
            is_active=False
        )
        self.client.login(username='anita', password='password')
        response = self.client.get(reverse('course-create', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
        }))
        self.assertContains(response, 'Pretty Smart')
        self.assertNotContains(response, 'Wonder Woman')
        self.assertNotContains(response, 'inactive_convener')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_inactive_convener_should_not_be_in_normal_user_detail_page(self):
        convener = UserF.create(**{
            'username': 'convener',
            'password': 'password',
            'first_name': 'Pretty',
            'last_name': 'Smart',
            'is_staff': True
        })
        convener_inactive = UserF.create(**{
            'username': 'inactive_convener',
            'password': 'password',
            'first_name': 'Wonder',
            'last_name': 'Woman',
            'is_staff': True
        })
        CourseConvenerF.create(
            user=convener,
            certifying_organisation=self.certifying_organisation
        )
        CourseConvenerF.create(
            user=convener_inactive,
            certifying_organisation=self.certifying_organisation,
            is_active=False
        )
        response = self.client.get(
            reverse('certifyingorganisation-detail', kwargs={
                'project_slug': self.project.slug,
                'slug': self.certifying_organisation.slug,
            })
        )
        self.assertContains(response, 'Pretty Smart')
        self.assertNotContains(response, 'Wonder Woman')
        self.assertNotContains(response, '[inactive]')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_inactive_convener_should_be_in_normal_user_detail_page(self):
        convener = UserF.create(**{
            'username': 'convener',
            'password': 'password',
            'first_name': 'Pretty',
            'last_name': 'Smart',
            'is_staff': True
        })
        convener_inactive = UserF.create(**{
            'username': 'inactive_convener',
            'password': 'password',
            'first_name': 'Wonder',
            'last_name': 'Woman',
            'is_staff': True
        })
        CourseConvenerF.create(
            user=convener,
            certifying_organisation=self.certifying_organisation
        )
        CourseConvenerF.create(
            user=convener_inactive,
            certifying_organisation=self.certifying_organisation,
            is_active=False
        )
        self.client.login(username='anita', password='password')
        response = self.client.get(
            reverse('certifyingorganisation-detail', kwargs={
                'project_slug': self.project.slug,
                'slug': self.certifying_organisation.slug,
            })
        )
        self.assertContains(response, 'Pretty Smart')
        self.assertContains(response, 'Wonder Woman')
        self.assertContains(response, '[inactive]')
