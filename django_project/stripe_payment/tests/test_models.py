# coding=utf-8
from django.test import TestCase
from stripe_payment.tests.model_factories import PaymentF


class TestPaymentCRUD(TestCase):
    """
    Tests CRUD Payment.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Project_create(self):
        """
        Tests Project model creation
        """
        model = PaymentF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_Project_read(self):
        """
        Tests Project model read
        """
        model = PaymentF.create(
            model_id=12,
            model_name=u'model_1',
            model_app_label=u'app_label_1',
            payment_id=u'payment_id_1',
            amount=12,
            currency=u'usd',
            description=u'description_1'
        )

        self.assertTrue(model.model_id == 12)
        self.assertTrue(model.model_name == 'model_1')
        self.assertTrue(model.model_app_label == 'app_label_1')
        self.assertTrue(model.payment_id == 'payment_id_1')
        self.assertTrue(model.amount == 12)
        self.assertTrue(model.currency == 'usd')
        self.assertTrue(model.description == 'description_1')

    def test_Project_update(self):
        """
        Tests Project model update
        """
        model = PaymentF.create()
        new_model_data = {
            'model_id': 12,
            'model_name': u'model_1',
            'model_app_label': u'app_label_1',
            'payment_id': u'payment_id_1',
            'amount': 12,
            'currency': u'usd',
            'description': u'description_1'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Project_delete(self):
        """
        Tests Project model delete
        """
        model = PaymentF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)
