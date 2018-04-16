# coding=utf-8
import logging
from mock import patch, MagicMock
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.test.client import Client
from base.tests.model_factories import ProjectF
from core.model_factories import UserF
from certification.tests.model_factories import (
    CourseF,
    CertifyingOrganisationF,
    CourseConvenerF,
    CertificateF,
    TrainingCenterF,
    CourseTypeF,
    AttendeeF
)


class TestCertificateView(TestCase):
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
        self.project = ProjectF.create()
        self.user = UserF.create(**{
            'username': 'anita',
            'password': 'password',
            'is_staff': True
        })
        self.user.set_password('password')
        self.user.save()

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
        self.certificate = CertificateF.create(
            course=self.course,
            attendee=self.attendee,
            author=self.user
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
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('__builtin__.open')
    def test_generate_certificate(self, mock_open, mock_make_dirs, mock_exists):
        mock_open.return_value = MagicMock(spec=file)
        mock_exists.return_value = True
        client = Client(HTTP_HOST='testserver')
        client.login(username='anita', password='password')
        response = client.get(reverse('print-certificate', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'course_slug': self.course.slug,
            'pk': self.attendee.pk
        }))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_detail_certificate(self):
        client = Client()
        response = client.get(reverse('certificate-details', kwargs={
            'project_slug': self.project.slug,
            'id': self.certificate.certificateID
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'certificate/detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
