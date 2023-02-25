""""
Serializers for the Transaction View.
"""
from rest_framework import serializers
from transaction.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """ Serializer for the transaction object. """

    class Meta:
        model = Transaction
        fields = ['from_client', 'to_client', 'value']
