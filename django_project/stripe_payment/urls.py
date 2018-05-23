# coding=utf-8
"""Urls for changelog application."""
from django.conf.urls import patterns, url
from stripe_payment.views.stripe_charge import StripeCharge

urlpatterns = patterns(
    '',
    url(regex='^payment/$',
        view=StripeCharge.as_view(),
        name='payment-view'),

)
