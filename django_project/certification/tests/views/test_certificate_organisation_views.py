# coding=utf-8
import logging
from django.urls import reverse
from django.test import TestCase, override_settings
from django.test.client import Client
from base.tests.model_factories import ProjectF
from core.model_factories import UserF
from certification.tests.model_factories import (
    CourseF,
    CertifyingOrganisationF,
    CourseConvenerF,
    CertificateF,
    CertificateTypeF,
    TrainingCenterF,
    CourseTypeF,
    AttendeeF,
    CertifyingOrganisationCertificateF
)


class TestCertificateOrganisationView(TestCase):
    """Test that certificate detail view and generating certificate works."""

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
            'username': 'user',
            'password': 'password',
            'is_staff': True,
        })
        self.user.set_password('password')
        self.user.save()

        self.user2 = UserF.create(**{
            'username': 'user2',
            'password': 'password',
            'is_staff': True,
            'first_name': 'User',
            'last_name': 'Last',
        })
        self.user.set_password('password')
        self.user.save()

        self.project = ProjectF.create(
            owner=self.user,
            project_representative=self.user2
        )
        self.certifying_organisation = \
            CertifyingOrganisationF.create()
        self.course_convener = CourseConvenerF.create()
        self.training_center = TrainingCenterF.create()
        self.course_type = CourseTypeF.create()
        self.course = CourseF.create(
            course_convener=self.course_convener,
            certifying_organisation=self.certifying_organisation,
            course_type=self.course_type,
            training_center=self.training_center
        )
        self.attendee = AttendeeF.create()
        self.certificate_type = CertificateTypeF.create()
        self.certificate = CertificateF.create(
            course=self.course,
            attendee=self.attendee,
            author=self.user,
            certificate_type=self.certificate_type
        )
        self.certifying_organisation_certificate = (
            CertifyingOrganisationCertificateF.create(
                author=self.user,
                certifying_organisation=self.certifying_organisation
            )
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.certificate.delete()
        self.attendee.delete()
        self.course.delete()
        self.training_center.delete()
        self.course_type.delete()
        self.course_convener.delete()
        self.certifying_organisation.delete()
        self.project.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_CertificateOrganisationCreateView_get(self):
        """Test get view"""
        self.client.login(username='user', password='password')
        response = self.client.get(
            reverse('issue-certificate-organisation', kwargs={
                'project_slug': self.project.slug,
                'organisation_slug': self.certifying_organisation.slug
            })
        )
        expected_template = [
            'certificate_organisation/create.html'
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, expected_template)
        self.assertEqual(response.context['certifying_organisation'],
                         self.certifying_organisation)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_CertificateOrganisationCreateView_post(self):
        """Test post view"""
        self.client.login(username='user', password='password')
        post_data = {}

        response = self.client.post(
            reverse('issue-certificate-organisation', kwargs={
                'project_slug': self.project.slug,
                'organisation_slug': self.certifying_organisation.slug
            }), post_data
        )

        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_OrganisationCertificateDetailView_get(self):
        """Test get view"""
        self.client.login(username='user', password='password')
        response = self.client.get(
            reverse('detail-certificate-organisation', kwargs={
                'project_slug': self.project.slug,
                'id': self.certifying_organisation_certificate.int_id
            })
        )
        expected_template = [
            'certificate_organisation/detail.html'
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, expected_template)
