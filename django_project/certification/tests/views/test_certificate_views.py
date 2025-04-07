# coding=utf-8
import tempfile
import logging
from mock import patch, MagicMock
from PIL import Image
from django.urls import reverse
from django.test.client import RequestFactory
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
    AttendeeF
)
from certification.views.certificate import (
    regenerate_certificate,
    regenerate_all_certificate
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
        self.user = UserF.create(**{
            'username': 'anita',
            'password': 'password',
            'is_staff': True,
        })
        self.user.set_password('password')
        self.user.save()

        self.user2 = UserF.create(**{
            'username': 'anita2',
            'password': 'password',
            'is_staff': True,
            'first_name': 'Anita',
            'last_name': 'Hapsari',
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
    @patch('builtins.open', create=True)
    def test_generate_certificate(
            self, mock_open, mock_make_dirs, mock_exists):
        mock_open.return_value = MagicMock()
        mock_exists.return_value = False
        client = Client(HTTP_HOST='testserver')
        client.login(username='anita', password='password')
        response = client.get(reverse('print-certificate', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'course_slug': self.course.slug,
            'pk': self.attendee.pk
        }))
        self.assertEqual(response.status_code, 200)

    def get_temporary_image(self, temp_file):
        size = (200, 200)
        color = (255, 0, 0, 0)
        image = Image.new("RGBA", size, color)
        image.save(temp_file, 'png')
        return temp_file

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @override_settings(VALID_DOMAIN=['testserver', ])
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', create=True)
    @patch('reportlab.lib.utils.ImageReader')
    def test_generate_certificate_with_signature(
            self, mock_open, mock_make_dirs, mock_exists, mock_image):
        mock_open.return_value = MagicMock()
        mock_exists.return_value = False
        mock_image.return_value = MagicMock()

        temp_file = tempfile.NamedTemporaryFile()
        test_image = self.get_temporary_image(temp_file)

        signature = test_image.name
        self.project.project_representative_signature = signature
        self.project.save()

        self.course_convener.signature = signature
        self.course_convener.save()

        client = Client(HTTP_HOST='testserver')
        client.login(username='anita', password='password')
        response = client.get(reverse('print-certificate', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'course_slug': self.course.slug,
            'pk': self.attendee.pk
        }))
        self.assertEqual(response.status_code, 200)
        self.project.project_representative_signature = None
        self.project.save()
        self.course_convener.signature = None
        self.course_convener.save()

    @override_settings(VALID_DOMAIN=['testserver', ])
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', create=True)
    def test_regenerate_certificate_allowed_user(
            self, mock_open, mock_make_dirs, mock_exists):
        mock_open.return_value = MagicMock()
        mock_exists.return_value = False
        request = RequestFactory(HTTP_HOST='testserver')
        request.user = self.user
        request.method = 'POST'
        request.META = {'HTTP_HOST': 'testserver'}
        response = regenerate_certificate(
            request,
            project_slug=self.project.slug,
            organisation_slug=self.certifying_organisation.slug,
            course_slug=self.course.slug,
            pk=self.attendee.pk
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', create=True)
    @patch('django.contrib.messages.success')
    @patch('os.remove')
    @patch('certification.views.certificate.generate_pdf')
    def test_regenerate_all_certificate_allowed_user(
            self, mock_open, mock_make_dirs,
            mock_exists, mock_message, mock_remove, mock_generate_pdf):
        mock_message.return_value = MagicMock()
        mock_open.return_value = MagicMock()
        mock_remove.return_value = MagicMock()
        mock_generate_pdf.return_value = MagicMock()
        mock_exists.return_value = False
        request = RequestFactory(HTTP_HOST='testserver')
        request.user = self.user
        request.method = 'POST'
        request.META = {'HTTP_HOST': 'testserver'}
        response = regenerate_all_certificate(
            request,
            project_slug=self.project.slug,
            organisation_slug=self.certifying_organisation.slug,
            course_slug=self.course.slug,
        )
        self.assertEqual(response.status_code, 302)

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
