from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from allauth.account.signals import (
        user_logged_in,
        user_signed_up
)

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeUser(models.Model):
    """Stripe User identity model."""

    user = models.OneToOneField(User)

    stripe_user_id = models.CharField(
        _('Stripe user ID'),
        max_length=200,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        if self.stripe_user_id:
            return str(self.stripe_user_id)
        else:
            return self.user.username


def stripe_call_back(sender, request, user, **kwargs):
    """Check if stripe user account has stripe id for user
        identification else assign one to that user.
    """

    stripe_user_account, created = StripeUser.objects.get_or_create(user=user)
    if created:
        if stripe_user_account.stripe_user_id is None or \
                stripe_user_account == '':
            new_stripe_user_id = stripe.Customer.create(email=user.email)
            stripe_user_account.stripe_user_id = new_stripe_user_id['id']
            stripe_user_account.save()
        else:
            stripe_user_account.stripe_user_id = ''


# django signal to attach the stripe ID to the currently signed up user.
user_signed_up.connect(stripe_call_back)

# django signal to attach the stripe ID to the currently logged in user.
user_logged_in.connect(stripe_call_back)
