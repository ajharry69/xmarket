from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from xauth.utils import get_wrapped_response

from .utils import stripe


class ClientSecretView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @staticmethod
    def post(request, format=None):
        try:
            amount = request.data.get('amount', 100)
            response = Response(
                data={'client_secret': stripe.Stripe().get_client_secret(amount), },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            response = Response(
                data={'error': e.args[0], },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return get_wrapped_response(response)
