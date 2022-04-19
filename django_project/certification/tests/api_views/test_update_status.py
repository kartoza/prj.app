from django.core import mail
from django.test import TestCase, override_settings, Client
from django.urls import reverse

from core.model_factories import UserF

from certification.models.certifying_organisation import CertifyingOrganisation
from certification.tests.model_factories import (
    StatusF,
    CertifyingOrganisationF,
    ProjectF
)


class TestUpdateStatus(TestCase):

    def setUp(self) -> None:
        self.approved_status = StatusF.create(name='Approved')
        self.rejected_status = StatusF.create(name='Rejected')
        self.pending_status = StatusF.create(name='Pending')

        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        self.user = UserF.create(**{
            'username': 'admin',
            'password': 'password',
            'email': 'test@test.com',
            'is_staff': True
        })
        self.project = ProjectF.create(
            owner=self.user
        )
        self.certifying_organisation = CertifyingOrganisationF.create(
            project=self.project,
            approved=False,
            rejected=False
        )
        self.certifying_organisation.organisation_owners.set([self.user])
        self.user.set_password('password')
        self.user.save()
        self.client.login(username='test', password='password')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_status_no_login(self):
        self.client.logout()
        response = self.client.post(
            reverse('certifyingorganisation-update-status', kwargs={
                'project_slug': self.project.slug,
                'slug': self.certifying_organisation.slug
            }), {
                'status': self.pending_status.id,
                'remarks': 'remarks'
            })
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_status(self):
        self.client.login(username='test', password='password')
        response = self.client.post(
            reverse('certifyingorganisation-update-status', kwargs={
                'project_slug': self.project.slug,
                'slug': self.certifying_organisation.slug
            }), {})
        self.assertEqual(response.status_code, 404)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_status_pending(self):
        certifying_organisation = CertifyingOrganisationF.create(
            project=self.project,
            approved=False,
            rejected=False,
            owner_message='test'
        )
        certifying_organisation.organisation_owners.set([self.user])
        self.client.login(username='admin', password='password')
        response = self.client.post(
            reverse('certifyingorganisation-update-status', kwargs={
                'project_slug': self.project.slug,
                'slug': certifying_organisation.slug
            }), {
                'status': self.pending_status.id,
                'remarks': 'remarks'
            })
        certifying_organisation = CertifyingOrganisation.objects.get(
            id=certifying_organisation.id
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            certifying_organisation.remarks,
            'remarks'
        )
        self.assertEqual(
            certifying_organisation.status,
            self.pending_status
        )
        self.assertEqual(
            certifying_organisation.owner_message,
            ''
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_status_approved(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(
            reverse('certifyingorganisation-update-status', kwargs={
                'project_slug': self.project.slug,
                'slug': self.certifying_organisation.slug
            }), {
                'status': self.approved_status.id,
                'remarks': 'remarks'
            })
        certifying_organisation = CertifyingOrganisation.objects.get(
            id=self.certifying_organisation.id
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            certifying_organisation.approved,
            True
        )
        self.assertEqual(
            certifying_organisation.status,
            self.approved_status
        )
        self.assertIn(
            'Your organisation is approved',
            mail.outbox[0].subject)
