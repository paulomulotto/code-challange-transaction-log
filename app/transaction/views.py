""""
Views for Transaction API
"""
from rest_framework import generics

from transaction.serializers import (
    TransactionSerializer
)


class CreateTransactionView(generics.CreateAPIView):
    """ Create a new transaction in the system. """
    serializer_class = TransactionSerializer