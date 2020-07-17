# coding=utf-8
import logging
from io import StringIO
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse
from certification.tests.model_factories import (
    ProjectF,
    UserF,
    CertifyingOrganisationF,
    StatusF
)


class TestCertifyingOrganisationView(TestCase):
    """Test that Certifying Organisation View works."""

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
        self.pending_certifying_organisation = CertifyingOrganisationF.create(
            name='test organisation rejected',
            project=self.project,
            approved=False,
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """

        self.certifying_organisation.delete()
        self.project.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_detail_view(self):
        client = Client()
        response = client.get(reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': self.certifying_organisation.slug
        }))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_detail_view_object_does_not_exist(self):
        client = Client()
        response = client.get(reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': 'random'
        }))
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('certifyingorganisation-detail', kwargs={
            'project_slug': 'random',
            'slug': self.certifying_organisation.slug
        }))
        self.assertEqual(response.status_code, 404)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_rejected_organisation_view_with_login(self):
        status = self.client.login(username='anita', password='password')
        self.assertTrue(status)
        response = self.client.get(
            reverse('certifyingorganisation-rejected-list', kwargs={
                'project_slug': self.project.slug,
            })
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_rejected_organisation_view_without_login(self):
        response = self.client.get(
            reverse('certifyingorganisation-rejected-list', kwargs={
                'project_slug': self.project.slug,
            })
        )
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_reject_organisation(self):
        status = self.client.login(username='anita', password='password')
        self.assertTrue(status)
        post_data = {
            'remarks': 'test rejection'
        }
        self.assertEqual(self.pending_certifying_organisation.approved, False)
        response = self.client.get(
            reverse('certifyingorganisation-reject', kwargs={
                'project_slug': self.project.slug,
                'slug': self.pending_certifying_organisation.slug
            }), post_data
        )
        self.assertEqual(response.status_code, 302)
        self.pending_certifying_organisation.refresh_from_db()
        self.assertEqual(self.pending_certifying_organisation.rejected, True)
        self.assertEqual(
            self.pending_certifying_organisation.remarks, 'test rejection')
        self.assertEqual(self.pending_certifying_organisation.approved, False)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_status_organisation(self):
        status = self.client.login(username='anita', password='password')
        self.assertTrue(status)
        status_object = StatusF.create()
        post_data = {
            'remarks': 'test update status',
            'status': status_object.id
        }
        self.assertEqual(self.pending_certifying_organisation.approved, False)
        response = self.client.post(
            reverse('certifyingorganisation-update-status', kwargs={
                'project_slug': self.project.slug,
                'slug': self.pending_certifying_organisation.slug
            }), post_data
        )
        self.assertEqual(response.status_code, 200)
        self.pending_certifying_organisation.refresh_from_db()
        self.assertEqual(
            self.pending_certifying_organisation.remarks, 'test update status')
        self.assertEqual(
            self.pending_certifying_organisation.status, status_object)
        self.assertEqual(self.pending_certifying_organisation.approved, False)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_get_status_list_no_login(self):
        response = self.client.get(
            reverse('get-status-list', kwargs={
                'project_slug': self.project.slug,
            })
        )
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_get_status_list_with_login(self):
        status = self.client.login(username='anita', password='password')
        self.assertTrue(status)
        status_object = StatusF.create(
            project=self.project
        )
        response = self.client.get(
            reverse('get-status-list', kwargs={
                'project_slug': self.project.slug,
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], status_object.name)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_status_command(self):
        out = StringIO()
        call_command('set_status_existing_organisation', stdout=out)
        self.certifying_organisation.refresh_from_db()
        self.pending_certifying_organisation.refresh_from_db()
        self.assertEquals(self.certifying_organisation.status.name, 'Approved')
        self.assertEquals(
            self.pending_certifying_organisation.status.name, 'Pending')
