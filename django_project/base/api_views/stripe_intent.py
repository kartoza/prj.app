import stripe
from rest_framework.views import APIView, Response
from django.conf import settings


class StripeIntent(APIView):
    """API to create a stripe intent. """

    def get(self, request, amount):
        currency = request.GET.get('currency', 'usd')
        stripe.api_key = (
            settings.STRIPE_LIVE_SECRET_KEY if settings.STRIPE_LIVE_MODE else
            settings.STRIPE_TEST_SECRET_KEY
        )
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )
        return Response(intent)
