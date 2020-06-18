from uuid import uuid4

import stripe
from django.conf import settings


class Stripe:
    __STRIPE_SETTING = settings.PAYMENT.get('STRIPE', {})
    __API_KEY = __STRIPE_SETTING.get('API_KEY', )

    def __init__(self, api_key: str = __API_KEY):
        stripe.api_key = api_key

    def get_client_secret(self, amount, currency: str = 'usd', **kwargs, ):
        intent = stripe.PaymentIntent.create(
            amount=round(float(amount)),
            currency=currency,
            idempotency_key=uuid4().hex,
            **kwargs,
        )
        return intent.to_dict_recursive()['client_secret']
