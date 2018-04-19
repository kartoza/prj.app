# coding=utf-8
from __future__ import absolute_import

from django.test import TestCase, override_settings
from django.test.client import Client
from ..model_factories import UserF
from base.tests.model_factories import ProjectF
from ..model_factories import (
	CertifyingOrganisationF,
	CourseF,
	CourseAttendeeF)


class TestGenerateCertificate(TestCase):
	"""Tests generation of a PDF certificate with expected content."""

	@override_settings(VALID_DOMAIN=['testerver', ])
	def setUp(self):
		"""Set up before test is run."""

		self.client = Client()
		self.client.post(
				'/set_language/', data={'language': 'en'})
		self.user = UserF.create(**{
			'username': 'Alison',
			'password': 'password',
			'is_staff': True,
		})

		self.user.set_password('password')
		self.user.save()
		self.project = ProjectF.create(certificate_credit=2)
		self.certifying_organisation = CertifyingOrganisationF.create(
				project=self.project)
		self.course = CourseF.create(certifying_organisation=self.certifying_organisation)
		self.attendee = CourseAttendeeF.create(course = \
			self.course)

	@override_settings(VALID_DOMAIN=['testerver', ])
	def tearDown(self):
		"""Clean up environment after test is done."""

		self.project.delete()
		self.certifying_organisation.delete()
		self.course.delete()
		self.attendee.delete()

	@override_settings(VALID_DOMAIN=['testerver', ])
	def test_generate_certificate_pdf(self):
		"""Test PDF object creation."""


		logged_in = self.client.login(username = 'Alison',
		                              password = 'password')
		self.assertTrue(logged_in)
