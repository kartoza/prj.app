# coding=utf-8

from django.test import TestCase
from django.test.client import Client
from core.model_factories import UserF
from base.tests.model_factories import ProjectF
from certification.tests.model_factories import (
    CourseF,
    CertifyingOrganisationF,
    CourseAttendeeF)
from certification.views import CertificateCreateView
from certification.forms import CertificateForm
from certification.models import Certificate


class TestCreditSystems(TestCase):
    """Test the credit systems in the certification."""

    def setUp(self):
        """
        In this test, a certificate is cost 3 credit.

        """

        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        self.user = UserF.create(**{
            'username': 'anita',
            'is_staff': True
        })
        self.user.set_password('password')
        self.user.save()
        self.project = ProjectF.create(certificate_credit=3)
        self.organisation = \
            CertifyingOrganisationF.create(
                project=self.project)
        self.course = CourseF.create(certifying_organisation=self.organisation)
        self.course_attendee = CourseAttendeeF.create(course=self.course)

    def tearDown(self):
        pass

    def test_issue_certificate_with_credit(self):
        """
        Test issue certificate when organisation is set to have 10 credits.

        """

        self.organisation = \
            CertifyingOrganisationF.create(
                project=self.project, organisation_credits=10)
        self.course = CourseF.create(certifying_organisation=self.organisation)

        # Issue certificate
        certificate_create = \
            CertificateCreateView(
                project_slug=self.project.slug,
                organisation_slug=self.organisation.slug,
                course_slug=self.course.slug)
        form = \
            CertificateForm(
                user=self.user,
                course=self.course,
                attendee=self.course_attendee.attendee,
            )

        response = certificate_create.form_valid(form)
        is_paid = form['is_paid'].value()
        self.assertEquals(response.status_code, 302)

        # Newly created object test
        certificate = \
            Certificate.objects.get(attendee=self.course_attendee.attendee)
        certificate.is_paid = is_paid

        # Test remaining credits in the organisation
        self.assertEquals(
            certificate.course.certifying_organisation.organisation_credits, 7)

        # Test status of the certificate
        self.assertEquals(certificate.is_paid, True)

        # Add another attendee
        course_attendee2 = CourseAttendeeF.create(course=self.course)

        # Issue another certificate
        certificate_create = \
            CertificateCreateView(
                project_slug=self.project.slug,
                organisation_slug=self.organisation.slug,
                course_slug=self.course.slug)
        form2 = \
            CertificateForm(
                user=self.user,
                course=self.course,
                attendee=course_attendee2.attendee,
            )
        response = certificate_create.form_valid(form2)
        is_paid = form2['is_paid'].value()
        self.assertEquals(response.status_code, 302)

        # Newly created object test
        certificate2 = \
            Certificate.objects.get(attendee=course_attendee2.attendee)
        certificate2.is_paid = is_paid

        self.assertEquals(
            certificate2.course.certifying_organisation.organisation_credits,
            4)
        self.assertEquals(certificate2.is_paid, True)

    def test_issue_certificate_without_credit(self):
        """Test when the organisation has no credit available."""

        # The organisation credit is set to 0
        self.organisation = \
            CertifyingOrganisationF.create(
                project=self.project, organisation_credits=0)
        self.course = CourseF.create(certifying_organisation=self.organisation)

        # Issue certificate
        certificate_create = \
            CertificateCreateView(
                project_slug=self.project.slug,
                organisation_slug=self.organisation.slug,
                course_slug=self.course.slug)
        form = \
            CertificateForm(
                user=self.user,
                course=self.course,
                attendee=self.course_attendee.attendee,
            )

        response = certificate_create.form_valid(form)
        is_paid = form['is_paid'].value()
        self.assertEquals(response.status_code, 302)

        # Newly created object test
        certificate = \
            Certificate.objects.get(attendee=self.course_attendee.attendee)
        certificate.is_paid = is_paid

        self.assertEquals(
            certificate.course.certifying_organisation.organisation_credits,
            -3)
        self.assertEquals(certificate.is_paid, False)
