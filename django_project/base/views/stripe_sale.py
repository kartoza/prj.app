# coding=utf-8
"""View for stripe payment processing."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def make_payment(request):
    """Process payment from user credit card."""

    publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    email = request.user.stripeuser.user.email
    if request.method == 'POST':
        token = request.POST['stripeToken']

        # create the charge on stripe servers
        # this will charge the user's card
        try:
            stripe.Charge.create(
                amount = settings.STRIPE_CHARGE_AMOUNT,
                currency = settings.STRIPE_CHARGE_CURRENCY,
                card = token,
                description = email
            )

        # The card has been declined
        except stripe.CardError:

            pass

    template = 'project/make_payment.html'
    context = {
        'publish_key': publishable_key
    }

    return render(request, template, context)
