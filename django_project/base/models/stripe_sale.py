import stripe
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Sale(models.Model):
    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)

        # bring in stripe, and get the api key from settings.py
        stripe.api_key = settings.STRIPE_API_KEY

        self.stripe = stripe

    # store the stripe charge id for this sale
    charge_id = models.CharField(
        _('Charge ID'),
        max_length=32,
        null=True,
        blank=True
    )

    charge_amount = models.DecimalField(
        _('Charge amount'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
        help_text=_('Amount charged on account in dollars'),
    )

    charge_stripe_id = models.CharField(
        _('Charge stripe ID'),
        max_length=50,
        null=True,
        blank=True
    )

    merchant_stripe_id = models.CharField(
        _('Mechant stripe ID'),
        max_length=50,
        null=True,
        blank=True
    )

    customer_stripe_id = models.CharField(
        _('Customer stripe ID'),
        max_length=50,
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        _('Timestamp'),
        default=timezone.now,
        blank=False,
        null=False,
        help_text=_('Enter the date and time when the payment was made.')
    )


    def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
        """
        Takes the price and credit card details: number, exp_month,
        exp_year, cvc.

        Returns a tuple: (Boolean, Class) where the boolean is if
        the charge was successful, and the class is response (or error)
        instance.
        """

        if self.charge_id:  # don't let this be charged twice!
            return False, Exception(message='Already charged.')

        try:
            response = self.stripe.Charge.create(
                amount=price_in_cents,
                currency=settings.CHARGE_CURRENCY,
                card={
                    'number': number,
                    'exp_month': exp_month,
                    'exp_year': exp_year,
                    'cvc': cvc,
                },

                description='Thank you for your purchase!')

            self.charge_id = response.id

        except self.stripe.CardError, ce:
            # charge failed
            return False, ce

        return True, response