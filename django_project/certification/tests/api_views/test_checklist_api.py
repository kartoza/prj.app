from django.test import TestCase, override_settings, Client

from core.model_factories import UserF
from base.tests.model_factories import ProjectF
from certification.tests.model_factories import CertifyingOrganisationF, ChecklistF
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
        self.api_url = '/en/{}/update-checklist-reviewer/'.format(
            self.project.slug
        )
        self.certifying_organisation = CertifyingOrganisationF.create(
            project=self.project,
            approved=False,
            rejected=False
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
        self.assertEqual(response.status_code, 400)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_submit_checklist(self):
        self.checklist = ChecklistF.create(
            project=self.project
        )
        data = {
            f'organisation': self.certifying_organisation.id,
            f'checklist-{self.checklist.id}': 'yes'
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
