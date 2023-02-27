""""
Account Views
"""
from rest_framework import generics, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AccountSerializer
from .models import Account


class CreateAccountView(generics.CreateAPIView):
    serializer_class = AccountSerializer


class BalanceView(APIView):
    """"
    View to see the Balance of an Account
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_id=None, format=None):
        """
        Return the balance of user account.
        """
        user = self.request.user
        account = Account.objects.get(
            client__user=user,
            business_id=business_id
        )
        return Response(
            {
                'number': account.number,
                'balance': account.balance
            }
        )
