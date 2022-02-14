# coding=utf-8
from unittest.mock import patch
from django.urls import reverse
from django.test import TestCase, override_settings
from django.test.client import Client
import logging
from core.model_factories import UserF
from base.tests.model_factories import ProjectF
from certification.tests.model_factories import (
    CertifyingOrganisationF,
    CourseConvenerF,
    TrainingCenterF,
    CourseTypeF,
    CertificateTypeF
)


class TestCertificatePreview(TestCase):
    """Test that certificate views work."""

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
            'is_staff': True
        })
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

        self.test_project = ProjectF.create()
        self.test_certifying_organisation = CertifyingOrganisationF.create()
        self.convener = CourseConvenerF.create()
        self.training_center = TrainingCenterF.create()
        self.course_type = CourseTypeF.create()
        self.certificate_type = CertificateTypeF.create()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.test_project.delete()
        self.convener.delete()
        self.training_center.delete()
        self.course_type.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_preview_certificate_no_data_posted_no_login(self):
        client = Client()
        response = client.get(reverse('preview-certificate', kwargs={
            'project_slug': self.test_project.slug,
            'organisation_slug': self.test_certifying_organisation.slug
        }))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_preview_certificate_no_data_posted(self):
        client = Client()
        client.login(username='anita', password='password')
        response = client.get(reverse('preview-certificate', kwargs={
            'project_slug': self.test_project.slug,
            'organisation_slug': self.test_certifying_organisation.slug
        }))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    @patch('certification.views.certificate.generate_pdf')
    def test_preview_certificate_with_posted_data(self, mock_gen_pdf):
        client = Client(HTTP_HOST='testserver')
        client.login(username='anita', password='password')
        post_data = {
            'course_convener': self.convener.pk,
            'training_center': self.training_center.pk,
            'course_type': self.course_type.pk,
            'start_date': '2018-01-01',
            'end_date': '2018-02-01',
            'template_certificate': ''
        }
        response = client.post(reverse('preview-certificate', kwargs={
            'project_slug': self.test_project.slug,
            'organisation_slug': self.test_certifying_organisation.slug
        }), post_data)
        self.assertEqual(response.status_code, 200)
        # Only 6 args in generate_pdf call,
        # Since there's no CertificateType id in POST body
        self.assertEqual(len(mock_gen_pdf.call_args[0]), 6)
        self.assertIn(self.test_project, mock_gen_pdf.call_args[0])
        self.assertNotIn(
            self.certificate_type.wording, mock_gen_pdf.call_args[0])

    @override_settings(VALID_DOMAIN=['testserver', ])
    @patch('certification.views.certificate.generate_pdf')
    def test_preview_certificate_with_posted_data_and_certificate_type(
            self, mock_gen_pdf):
        client = Client(HTTP_HOST='testserver')
        client.login(username='anita', password='password')
        post_data = {
            'course_convener': self.convener.pk,
            'training_center': self.training_center.pk,
            'course_type': self.course_type.pk,
            'start_date': '2018-01-01',
            'end_date': '2018-02-01',
            'template_certificate': '',
            'certificate_type': self.certificate_type.id
        }
        response = client.post(reverse('preview-certificate', kwargs={
            'project_slug': self.test_project.slug,
            'organisation_slug': self.test_certifying_organisation.slug
        }), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mock_gen_pdf.call_args[0]), 7)
        self.assertIn(self.test_project, mock_gen_pdf.call_args[0])
        self.assertIn(self.certificate_type.wording, mock_gen_pdf.call_args[0])


    @override_settings(VALID_DOMAIN=['testserver', ])
    @patch('certification.views.certificate.generate_pdf')
    def test_preview_certificate_with_posted_data_cert_type_not_found(
            self, mock_gen_pdf):
        client = Client(HTTP_HOST='testserver')
        client.login(username='anita', password='password')
        post_data = {
            'course_convener': self.convener.pk,
            'training_center': self.training_center.pk,
            'course_type': self.course_type.pk,
            'start_date': '2018-01-01',
            'end_date': '2018-02-01',
            'template_certificate': '',
            'certificate_type': 99999
        }
        response = client.post(reverse('preview-certificate', kwargs={
            'project_slug': self.test_project.slug,
            'organisation_slug': self.test_certifying_organisation.slug
        }), post_data)
        self.assertEqual(response.status_code, 200)
        # Only 6 args in generate_pdf call,
        # Since there's the CertificateType id doesn't exist
        self.assertEqual(len(mock_gen_pdf.call_args[0]), 6)
        self.assertIn(self.test_project, mock_gen_pdf.call_args[0])
        self.assertNotIn(
            self.certificate_type.wording, mock_gen_pdf.call_args[0])
