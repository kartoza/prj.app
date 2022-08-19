# coding=utf-8
from django.urls import reverse
from django.test import TestCase, override_settings
from django.test.client import Client
from base.tests.model_factories import ProjectF
from certification.tests.model_factories import (
    CertifyingOrganisationF,
    TrainingCenterF,
    CourseF,
    CourseConvenerF,
    CourseTypeF,
    AttendeeF,
    CertificateF
)
from core.model_factories import UserF
import logging


class TestAttendeeView(TestCase):

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self) -> None:
        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        self.project = ProjectF.create()
        self.certifying_organisation = CertifyingOrganisationF.create(
            project=self.project)
        self.training_center = TrainingCenterF.create(
            certifying_organisation=self.certifying_organisation)
        self.course_convener = CourseConvenerF.create(
            certifying_organisation=self.certifying_organisation)
        self.course_type = CourseTypeF.create(
            certifying_organisation=self.certifying_organisation)
        self.course = CourseF.create(
            certifying_organisation=self.certifying_organisation,
            training_center=self.training_center,
            course_convener=self.course_convener,
            course_type=self.course_type
        )
        self.user = UserF.create(**{
            'username': 'user',
            'password': 'password',
            'is_staff': True
        })
        self.user.set_password('password')
        self.user.save()
        self.attendee = AttendeeF.create(
            certifying_organisation=self.certifying_organisation)
        self.certificate = CertificateF.create(
            course=self.course,
            attendee=self.attendee,
            author=self.user)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_AttendeeUpdateView_with_login(self):
        status = self.client.login(username='user', password='password')
        self.assertTrue(status)
        url = reverse('attendee-update', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'course_slug': self.course.slug,
            'pk': self.attendee.pk
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCourseAttendeeView(TestCase):
    """Tests that attendee and course attendee view works."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.project = ProjectF.create()
        self.certifying_organisation = \
            CertifyingOrganisationF.create(project=self.project)
        self.training_center = \
            TrainingCenterF.create(
                certifying_organisation=self.certifying_organisation)
        self.course_convener = \
            CourseConvenerF.create(
                certifying_organisation=self.certifying_organisation)
        self.course_type = \
            CourseTypeF.create(
                certifying_organisation=self.certifying_organisation)
        self.course = CourseF.create(
            certifying_organisation=self.certifying_organisation,
            training_center=self.training_center,
            course_convener=self.course_convener,
            course_type=self.course_type
        )
        self.user = UserF.create(**{
            'username': 'anita',
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
        self.certifying_organisation.delete()
        self.training_center.delete()
        self.course_convener.delete()
        self.course_type.delete()
        self.course.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_AttendeeCreateView_no_login(self):
        response = self.client.get(reverse('attendee-create', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': self.course.slug
        }))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_AttendeeCreateView_with_login(self):
        status = self.client.login(username='anita', password='password')
        self.assertTrue(status)
        url = reverse('attendee-create', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': self.course.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'attendee/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_AttendeeAndCourseAttendeeCreate_with_login(self):
        """
        Test create attendee that automatically create course attendee
        from this newly created attendee object.

        """
        self.client.login(username='anita', password='password')
        post_data = {
            'firstname': u'Test',
            'surname': u'Course-Attendee',
            'email': u'test@test.com',
            'certifying_organisation': self.certifying_organisation.id,
            'add_to_course': True,
        }
        response = self.client.post(reverse('attendee-create', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': self.course.slug
        }), post_data)
        self.assertRedirects(
            response,
            reverse(
                'course-detail',
                kwargs={
                    'project_slug': self.project.slug,
                    'organisation_slug': self.certifying_organisation.slug,
                    'slug': self.course.slug
                }))

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_AttendeeOnlyCreate_with_login(self):
        """
        Test create attendee only.

        """
        self.client.login(username='anita', password='password')
        post_data = {
            'firstname': u'Test',
            'surname': u'Attendee',
            'email': u'test@test.com',
            'certifying_organisation': self.certifying_organisation.id,
        }
        response = self.client.post(reverse('attendee-create', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'slug': self.course.slug
        }), post_data)
        self.assertRedirects(
            response,
            reverse(
                'courseattendee-create',
                kwargs={
                    'project_slug': self.project.slug,
                    'organisation_slug': self.certifying_organisation.slug,
                    'slug': self.course.slug
                }))
