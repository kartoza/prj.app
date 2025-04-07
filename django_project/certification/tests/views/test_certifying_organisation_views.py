# coding=utf-8
import logging
from io import StringIO

from django.contrib.sessions.backends.db import SessionStore
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse

from certification.models import (
    ORGANIZATION_OWNER, REVIEWER, OrganisationChecklist
)
from certification.tests.model_factories import (
    ProjectF,
    UserF,
    CertifyingOrganisationF,
    StatusF, ChecklistF, OrganisationChecklistF, ExternalReviewerF
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
    def test_list_pending_view(self):
        client = Client()
        client.login(username='anita', password='password')
        response = client.get(
            reverse('pending-certifyingorganisation-list',
                    kwargs={
                        'project_slug': self.project.slug
                    }) + '?ready=false')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pending'], True)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_list_pending_json(self):
        client = Client()
        client.login(username='anita', password='password')

        pending_status = StatusF.create(
            name='pending'
        )
        pending_certifying_organisation = CertifyingOrganisationF.create(
            name='test organisation pending',
            project=self.project,
            approved=False,
            status=pending_status
        )
        response = client.get(
            reverse('certifyingorganisation-list-json',
                    kwargs={
                        'project_slug': self.project.slug
                    }) + '?ready=False&approved=False')
        self.assertEqual(response.status_code, 200)

        # Empty and invalid parameters should be handled
        # and return the same result as above
        response_param_ivalid = client.get(
            reverse('certifyingorganisation-list-json',
                    kwargs={
                        'project_slug': self.project.slug
                    }) + '?ready=no&approved=')
        self.assertEqual(response_param_ivalid.status_code, 200)

        json_response = response.json()
        json_response_invalid_param = response_param_ivalid.json()
        self.assertEqual(json_response, json_response_invalid_param)

        self.assertEqual(
            len(json_response['data']),
            1
        )
        self.assertEqual(
            json_response['data'][0][1],
            str(pending_certifying_organisation.creation_date)
        )
        self.assertEqual(
            json_response['data'][0][2],
            str(pending_certifying_organisation.update_date)
        )
        self.assertIn(
            pending_certifying_organisation.name,
            json_response['data'][0][0]
        )
        response = client.get(
            reverse('certifyingorganisation-list-json',
                    kwargs={
                        'project_slug': self.project.slug
                    }) + '?ready=True')
        json_response = response.json()
        self.assertEqual(
            len(json_response['data']),
            1
        )
        self.assertIn(
            self.pending_certifying_organisation.name,
            json_response['data'][0][0]
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_list_approved_json(self):
        client = Client()
        client.login(username='anita', password='password')
        approved_certifying_organisation = CertifyingOrganisationF.create(
            name='test organisation pending',
            project=self.project,
            approved=True
        )
        response = client.get(
            reverse('certifyingorganisation-list-json',
                    kwargs={
                        'project_slug': self.project.slug
                    }) + '?approved=True')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(
            len(json_response['data']),
            2
        )
        self.assertEqual(
            json_response['data'][1][1],
            str(approved_certifying_organisation.creation_date)
        )
        self.assertEqual(
            json_response['data'][1][2],
            str(approved_certifying_organisation.update_date)
        )
        self.assertIn(
            approved_certifying_organisation.name,
            json_response['data'][1][0]
        )
        self.assertIn(
            self.certifying_organisation.name,
            json_response['data'][0][0]
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_create_view(self):
        client = Client()
        client.login(username='anita', password='password')
        ChecklistF.create(
            project=self.project,
            target=ORGANIZATION_OWNER,
            active=True
        )
        response = client.get(
            reverse('certifyingorganisation-create', kwargs={
                'project_slug': self.project.slug
            }))
        self.assertTrue(len(response.context_data['available_checklist']) > 0)
        self.assertEqual(response.context_data['the_project'], self.project)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_create_view_post(self):
        client = Client()
        client.login(username='anita', password='password')
        checklist = ChecklistF.create(
            project=self.project,
            target=ORGANIZATION_OWNER,
            active=True
        )
        org_slug = 'org_name'
        post_data = {
            'name': org_slug,
            'organisation_email': 'org@test.com',
            'address': 'city',
            'country': 'ID',
            'organisation_phone': '1111111',
            'organisation_owners': self.user.id,
            'project': self.project.id,
            f'checklist-{checklist.id}': 'yes',
            f'textarea-{checklist.id}': 'test',
        }
        response = client.post(
            reverse('certifyingorganisation-create', kwargs={
                'project_slug': self.project.slug
            }), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            OrganisationChecklist.objects.filter(
                submitter=self.user,
                checklist=checklist,
                checked=True
            ).exists()
        )
        self.assertIn(
            f'/en/{self.project.slug}/certifyingorganisation/{org_slug}/',
            mail.outbox[0].body)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_view(self):
        client = Client()
        client.login(username='anita', password='password')
        pending_certifying_organisation = CertifyingOrganisationF.create(
            project=self.project,
            approved=False
        )
        pending_certifying_organisation.organisation_owners.set(
            [self.user]
        )
        response = client.get(
            reverse('certifyingorganisation-update', kwargs={
                'slug': pending_certifying_organisation.slug,
                'project_slug': self.project.slug,
            }))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Message to validator', response.content)
        self.assertEqual(
            response.context_data['certifyingorganisation'],
            pending_certifying_organisation
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_detail_view_pending(self):
        client = Client()
        client.login(username='anita', password='password')
        pending_certifying_organisation = CertifyingOrganisationF.create(
            project=self.project,
            approved=True
        )
        s = SessionStore()
        s.create()
        ExternalReviewerF.create(
            certifying_organisation=pending_certifying_organisation,
            email='er1@email.com',
            session_key=s.session_key
        )
        ExternalReviewerF.create(
            certifying_organisation=pending_certifying_organisation,
            email='er2@email.com'
        )
        pending_certifying_organisation.organisation_owners.set(
            [self.user]
        )
        self.checklist = ChecklistF.create(
            project=self.project,
            target=REVIEWER,
            active=True
        )
        checklist_owner = ChecklistF.create(
            project=self.project,
            target=ORGANIZATION_OWNER,
            active=True
        )
        OrganisationChecklistF.create(
            checklist=self.checklist,
            organisation=pending_certifying_organisation,
            checked=True
        )
        OrganisationChecklistF.create(
            checklist=checklist_owner,
            organisation=pending_certifying_organisation,
            checked=True
        )
        response = client.get(reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': pending_certifying_organisation.slug
        }))
        self.assertEqual(
            len(response.context_data['available_checklist']), 1)
        self.assertEqual(
            len(response.context_data['submitted_checklist']), 2)
        self.assertEqual(
            len(response.context_data['history']), 1)
        self.assertEqual(
            response.context_data['user_can_create'], True)
        self.assertEqual(
            response.context_data['user_can_delete'], True)
        self.assertEqual(
            len(response.context_data['external_reviewers']), 1)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_detail_view_pending_external_reviewer(self):
        s = SessionStore()
        s.create()
        ExternalReviewerF.create(
            certifying_organisation=self.pending_certifying_organisation,
            email='er1@email.com',
            session_key=s.session_key
        )
        response = self.client.get(
            reverse('certifyingorganisation-detail', kwargs={
                'project_slug': self.project.slug,
                'slug': self.pending_certifying_organisation.slug
            }).replace('en-us', 'en') + f'?s={s.session_key}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data['user_can_update_status'])

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
    def test_get_archive_view(self):
        client = Client()
        client.login(username='anita', password='password')
        response = client.get(
            reverse('certifyingorganisation-toogle-archive', kwargs={
                'project_slug': self.project.slug,
                'slug': self.certifying_organisation.slug,
                'toogle_archive': 'archive'
            }))
        self.assertEqual(response.status_code, 200)
        self.assertIn('archive', response.context['toogle_archive'])
        self.assertEqual(
            response.context['certifyingorganisation'],
            self.certifying_organisation
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_get_unarchive_view(self):
        client = Client()
        client.login(username='anita', password='password')
        response = client.get(
            reverse('certifyingorganisation-toogle-archive', kwargs={
                'project_slug': self.project.slug,
                'slug': self.certifying_organisation.slug,
                'toogle_archive': 'unarchive'
            }))
        self.assertEqual(response.status_code, 200)
        self.assertIn('unarchive', response.context['toogle_archive'])
        self.assertEqual(
            response.context['certifyingorganisation'],
            self.certifying_organisation
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_post_archive_view(self):
        client = Client()
        client.login(username='anita', password='password')
        response = client.post(
            reverse('certifyingorganisation-toogle-archive', kwargs={
                'project_slug': self.project.slug,
                'slug': self.certifying_organisation.slug,
                'toogle_archive': 'archive'
            }))
        self.assertEqual(response.status_code, 302)
        self.certifying_organisation.refresh_from_db()
        self.assertTrue(self.certifying_organisation.is_archived)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_post_unarchive_view(self):
        client = Client()
        client.login(username='anita', password='password')
        self.certifying_organisation.is_archived = True
        self.certifying_organisation.save()
        response = client.post(
            reverse('certifyingorganisation-toogle-archive', kwargs={
                'project_slug': self.project.slug,
                'slug': self.certifying_organisation.slug,
                'toogle_archive': 'unarchive'
            }))
        self.assertEqual(response.status_code, 302)
        self.certifying_organisation.refresh_from_db()
        self.assertFalse(self.certifying_organisation.is_archived)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_status_command(self):
        out = StringIO()
        call_command('set_status_existing_organisation', stdout=out)
        self.certifying_organisation.refresh_from_db()
        self.pending_certifying_organisation.refresh_from_db()
        self.assertEquals(self.certifying_organisation.status.name, 'Approved')
        self.assertEquals(
            self.pending_certifying_organisation.status.name, 'Pending')
