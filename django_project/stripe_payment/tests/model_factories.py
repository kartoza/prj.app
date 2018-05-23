# coding=utf-8
"""Factories for building model instances for testing."""

import factory

from stripe_payment.models import Payment
from core.model_factories import UserF


class PaymentF(factory.django.DjangoModelFactory):
    """Payment model factory."""

    class Meta:
        model = Payment

    user = factory.SubFactory(UserF)
    model_id = 1
    model_name = factory.sequence(lambda n: u'Model name %s' % n)
    model_app_label = factory.sequence(lambda n: u'Model app label %s' % n)
    payment_id = factory.sequence(lambda n: u'%s' % n)
    amount = 12.0
    currency = u'usd'
    description = u'This is only for testing'
    note = u'This is only for testing'
