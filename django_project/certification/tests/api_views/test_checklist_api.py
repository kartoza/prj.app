from django.test import TestCase, override_settings, Client
from django.urls import reverse

from certification.models import CertifyingOrganisation
from core.model_factories import UserF
from base.tests.model_factories import ProjectF
from certification.tests.model_factories import (
    CertifyingOrganisationF, ChecklistF, ExternalReviewerF
)
from certification.models.organisation_checklist import OrganisationChecklist


class TestChecklistApi(TestCase):

    def setUp(self) -> None:
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
            name='test project',
            owner=self.user
        )
        self.user.set_password('password')
        self.user.save()
        self.certifying_organisation = CertifyingOrganisationF.create(
            project=self.project,
            approved=False,
            rejected=False
        )
        self.api_url = '/en/{0}/update-checklist-reviewer/{1}/'.format(
            self.project.slug,
            self.certifying_organisation.slug
        )
        self.certifying_organisation.organisation_owners.set([self.user])

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_submit_checklist_no_login(self):
        response = self.client.post(self.api_url)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_submit_checklist_no_data(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(self.api_url, {})
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_submit_checklist(self):
        self.checklist = ChecklistF.create(
            project=self.project
        )
        checklist_2 = ChecklistF.create(
            project=self.project,
            show_text_box=True
        )
        checklist_3 = ChecklistF.create(
            project=self.project,
            show_text_box=True
        )
        checklist_4 = ChecklistF.create(
            project=self.project,
            show_text_box=True
        )
        data = {
            f'checklist-{self.checklist.id}': 'yes',
            f'textarea-{checklist_2.id}': 'test',
            'checklist-99999': 'yes',
            f'textarea-{checklist_3.id}': 'test',
            f'checklist-{checklist_3.id}': 'yes',
            f'checklist-{checklist_4.id}': 'yes',
            f'textarea-{checklist_4.id}': 'test',
        }
        self.client.login(username='admin', password='password')
        response = self.client.post(self.api_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            OrganisationChecklist.objects.filter(
                organisation=self.certifying_organisation,
                checklist=self.checklist,
                checklist_question=self.checklist.question,
                submitter=self.user,
                checked=True
            ).exists()
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_submit_checklist_external_reviewer(self):
        from django.contrib.sessions.backends.db import SessionStore
        s = SessionStore()
        s.create()
        ExternalReviewerF.create(
            session_key=s.session_key,
            email='external@email.com',
            certifying_organisation=self.certifying_organisation
        )
        self.checklist = ChecklistF.create(
            project=self.project
        )
        data = {
            f'checklist-{self.checklist.id}': 'yes'
        }
        url = reverse('update-checklist-reviewer', kwargs={
            'project_slug': self.project.slug,
            'slug': self.certifying_organisation.slug
        }) + '?s=' + s.session_key
        url = url.replace('/en-us/', '/en/')
        response = self.client.post(
            url, data)
        self.assertEqual(response.status_code, 302)
        certifying_organisation = CertifyingOrganisation.objects.get(
            id=self.certifying_organisation.id
        )
        checklist_org = OrganisationChecklist.objects.filter(
            organisation=certifying_organisation
        )
        self.assertIsNotNone(
            checklist_org.last().external_submitter
        )
        self.assertIsNone(
            checklist_org.last().submitter
        )
        self.assertIn(
            'Checklist updated by external reviewer (external@email.com)',
            certifying_organisation.history.latest().history_change_reason
        )
