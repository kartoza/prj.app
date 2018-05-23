__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '16/05/18'

import stripe
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from stripe_payment.models import Payment


class StripeCharge(LoginRequiredMixin, View):
    """View for topup credit."""

    def charge(self, source, email, amount, description, currency):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # create customer
        response = stripe.Customer.create(
            api_key=settings.STRIPE_SECRET_KEY,
            description=description,
            email=email,
            source=source
        )

        # create charge
        amount = float(amount) * 100
        amount = int(amount)
        payment = stripe.Charge.create(
            amount=amount,
            currency=currency,
            customer=response['id'],
            description=description
        )
        return payment

    def post(self, request, *args, **kwargs):
        """Post request payment to stripe account.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict
        """
        source = request.POST.get('id')
        amount = request.POST.get('amount')
        model_id = request.POST.get('model_id')
        model_name = request.POST.get('model_name')
        model_app_label = request.POST.get('model_app_label')
        currency = request.POST.get('currency')

        for field in ['id', 'amount', 'currency']:
            if not request.POST.get(field):
                return HttpResponseBadRequest('%s' % field)

        description = request.POST.get('description')

        user = request.user
        email = request.user.email

        payment = self.charge(source, email, amount, description, currency)
        payment_id = payment.id

        Payment.objects.create(
            user=user,
            model_id=model_id,
            model_name=model_name,
            model_app_label=model_app_label,
            payment_id=payment_id,
            amount=amount,
            currency=currency,
            description=description
        )
        return HttpResponse('')
