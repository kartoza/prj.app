from django.test import TestCase

from base.tests.model_factories import ProjectF
from certification.models import CertifyingOrganisation
from certification.tests.model_factories import (
    CertifyingOrganisationF, StatusF
)
from core.model_factories import UserF
from certification.forms import CertifyingOrganisationForm


class TestCertifyingOrganisationForm(TestCase):

    def setUp(self):
        self.user = UserF.create(**{
            'username': 'admin',
            'password': 'password',
            'is_staff': True
        })
        self.project = ProjectF.create()
        self.status = StatusF.create(name='pending')
        self.certifying_organisation = CertifyingOrganisationF.create(
            project=self.project,
            approved=False,
            rejected=False,
            status=self.status
        )
        self.certifying_organisation.organisation_owners.set([self.user])
        self.user.set_password('password')
        self.user.save()
        self.client.login(username='admin', password='password')

    def test_update_form(self):
        form_title = 'Update form'
        form = CertifyingOrganisationForm(
            user=self.user,
            project=self.project,
            form_title=form_title,
            show_owner_message=True
        )
        self.assertEqual(
            form.helper.layout.fields[0].legend,
            form_title
        )
        self.assertEqual(
            form.fields['owner_message'].label,
            'Message to validator'
        )
        self.assertFalse(form.is_valid())

        data = {
            'name': 'Updated organisation',
            'organisation_email': 'test@test.com',
            'address': 'Address',
            'organisation_phone': '12121212',
            'organisation_owners': [self.user.id],
            'owner_message': 'test',
            'project': self.project.id
        }
        form = CertifyingOrganisationForm(
            instance=self.certifying_organisation,
            user=self.user,
            project=self.project,
            form_title=form_title,
            show_owner_message=True,
            data=data
        )
        self.assertTrue(form.is_valid())
        form.save()
        certifying_organisation = (
            CertifyingOrganisation.objects.get(
                id=self.certifying_organisation.id
            )
        )
        self.assertEqual(
            certifying_organisation.status,
            None
        )
