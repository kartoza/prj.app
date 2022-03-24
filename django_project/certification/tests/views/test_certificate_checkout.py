from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings, Client
from django.urls import reverse
from djstripe.models import Customer

from base.tests.model_factories import ProjectF
from certification.models import CertifyingOrganisation
from certification.tests.model_factories import CertifyingOrganisationF
from core.model_factories import UserF, CustomerF

FAKE_SESSION = {
    "id": "txn_16g5h62eZvKYlo2CQ2AHA89s",
    "metadata": {
        "organisation_id": "1",
        "credits_quantity": 100,
    },
    "payment_status": "paid",
}


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class CertificateCheckoutTest(TestCase):

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        self.client = Client()
        self.client.post(
            '/set_language/', data={'language': 'en'})
        self.project = ProjectF.create()
        self.certifying_organisation = (
            CertifyingOrganisationF.create(
                project=self.project,
                organisation_credits=0
            )
        )
        self.user = UserF.create(**{
            'username': 'test',
            'password': 'password',
            'email': 'test@test.com',
            'is_staff': True
        })
        self.user.set_password('password')
        self.user.save()
        self.project.certification_managers.add(self.user)
        self.customer = CustomerF.create(**{
            'name': 'test',
            'email': 'test@test.com'
        })

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.certifying_organisation.delete()
        self.user.delete()
        Customer.objects.raw(
            "DELETE FROM djstripe_customer WHERE "
            "djstripe_customer.id = '{}'".format(
                    self.customer.id))

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_checkout_without_login(self):
        url = '{0}?org={1}'.format(
            reverse('checkout'),
            self.certifying_organisation.id
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_checkout_view_missing_params(self):
        self.client.login(username='test', password='password')
        url = '{}'.format(reverse('checkout'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        url = '{0}?org={1}'.format(
            reverse('checkout'),
            self.certifying_organisation.id
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @patch(
        "stripe.checkout.Session.create",
        return_value=FAKE_SESSION,
        autospec=True,
    )
    @override_settings(VALID_DOMAIN=['testserver'])
    def test_checkout_view(self, session_create_mock):
        self.client.login(username='test', password='password')
        fake_session = Struct(**FAKE_SESSION)
        credits_quantity = 10
        fake_session.metadata['organisation_id'] = (
              self.certifying_organisation.id
        )
        fake_session.metadata['credits_quantity'] = (
            credits_quantity
        )
        session_create_mock.return_value = fake_session
        url = '{0}?org={1}&unit={2}&total=200'.format(
            reverse('checkout'),
            self.certifying_organisation.id,
            credits_quantity
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('checkout.html' in response.template_name)
        self.assertEqual(
            response.context_data['CHECKOUT_SESSION_ID'], fake_session.id)

    @patch(
        "stripe.checkout.Session.create",
        return_value=FAKE_SESSION,
        autospec=True,
    )
    @patch(
        "stripe.checkout.Session.retrieve",
        return_value=FAKE_SESSION,
        autospec=True,
    )
    @override_settings(VALID_DOMAIN=['testserver'])
    def test_checkout_success_view(
            self, session_retrieve_mock, session_create_mock):
        self.client.login(username='test', password='password')
        fake_session = FAKE_SESSION
        credits_quantity = 10
        fake_session['metadata']['organisation_id'] = (
            self.certifying_organisation.id
        )
        fake_session['metadata']['credits_quantity'] = (
            credits_quantity
        )
        session_retrieve_mock.return_value = fake_session
        fake_session_struct = Struct(**fake_session)
        session_create_mock.return_value = fake_session_struct
        url = '{0}?org={1}&unit={2}&total=200'.format(
            reverse('checkout'),
            self.certifying_organisation.id,
            credits_quantity
        )
        response = self.client.get(url)

        url = '{0}?session_id={1}'.format(
            reverse('checkout-success'),
            response.context_data['CHECKOUT_SESSION_ID']
        )
        response = self.client.get(url)
        self.assertTrue(response.status_code, 302)
        self.assertTrue(
            CertifyingOrganisation.objects.get(
                id=self.certifying_organisation.id).organisation_credits,
            credits_quantity)
        self.assertTrue('Top Up Successful' in mail.outbox[0].subject)
