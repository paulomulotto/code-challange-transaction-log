""""
Views for Transaction API
"""
from rest_framework import generics
from django.db.models import Q
from .models import Transaction

from account.transaction.serializers import (
    TransactionSerializer
)


class CreateTransactionView(generics.CreateAPIView):
    """ Create a new transaction in the system. """
    serializer_class = TransactionSerializer


class ListTransactionView(generics.ListAPIView):
    """ List Transactions """
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(
            Q(from_account__client__user=user) |
            Q(from_account__client__user=user)
        )
        return queryset
