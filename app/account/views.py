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

    def get(self, request):
        """
        Return the balance of user account.
        """
        user = self.request.user
        business_id = self.request.query_params.get('business_id')
        if business_id:
            account = Account.objects.get(
                client__user=user,
                business_id=business_id
            )
        else:
            account = Account.objects.get(
                client__user=user,
                business__isnull=True
            )
        return Response(
            {
                'number': account.number,
                'balance': account.balance
            }
        )
