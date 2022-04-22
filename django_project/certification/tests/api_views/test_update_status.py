from django.core import mail
from django.test import TestCase, override_settings, Client
from django.urls import reverse

from core.model_factories import UserF

from certification.models.certifying_organisation import CertifyingOrganisation
from certification.tests.model_factories import (
    StatusF,
    CertifyingOrganisationF,
    ProjectF, ExternalReviewerF
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
        self.user.set_password('password')
        self.user.save()

        self.project_owner = UserF.create(**{
            'username': 'owner',
            'password': 'password',
            'email': 'owner@test.com',
            'is_staff': False
        })
        self.project_owner.set_password('password')
        self.project_owner.save()

        self.project = ProjectF.create(
            owner=self.project_owner
        )
        self.certifying_organisation = CertifyingOrganisationF.create(
            project=self.project,
            approved=False,
            rejected=False
        )
        self.manager = UserF.create(**{
            'username': 'manager',
            'password': 'password',
            'email': 'manager@test.com',
            'is_staff': False
        })
        self.manager.set_password('password')
        self.manager.save()

        self.api_url = reverse('certifyingorganisation-update-status', kwargs={
            'project_slug': self.project.slug,
            'slug': self.certifying_organisation.slug
        }).replace('en-us', 'en')

        self.certifying_organisation.organisation_owners.set([self.user])
        self.project.certification_managers.set([self.manager])
        self.client.login(username='test', password='password')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_status_access(self):
        data = {
            'status': self.pending_status.id,
            'remarks': 'remarks'
        }

        # Admin/staff user
        self.client.login(
            username=self.user.username,
            password='password'
        )
        response = self.client.post(self.api_url, data)
        self.assertTrue(response.status_code, 200)

        # Project owner
        self.client.login(
            username=self.project_owner.username,
            password='password'
        )
        response = self.client.post(self.api_url, data)
        self.assertTrue(response.status_code, 200)

        # Certification manager
        self.client.login(
            username=self.manager.username,
            password='password'
        )
        response = self.client.post(self.api_url, data)
        self.assertTrue(response.status_code, 200)

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
        response = self.client.post(self.api_url, {})
        self.assertEqual(response.status_code, 302)

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
            }).replace('en-us', 'en'), {
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
            self.api_url, {
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

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_status_external_reviewer(self):
        from django.contrib.sessions.backends.db import SessionStore
        s = SessionStore()
        s.create()
        ExternalReviewerF.create(
            session_key=s.session_key,
            email='external@email.com',
            certifying_organisation=self.certifying_organisation
        )
        url = self.api_url + '?s=' + s.session_key
        url = url.replace('/en-us/', '/en/')
        response = self.client.post(
            url, {
                'status': self.pending_status.id,
                'remarks': 'remarks'
            })
        self.assertEqual(response.status_code, 200)
        certifying_organisation = CertifyingOrganisation.objects.get(
            id=self.certifying_organisation.id
        )
        self.assertIn(
            'Status updated to Pending by external '
            'reviewer (external@email.com)',
            certifying_organisation.history.latest().history_change_reason
        )
