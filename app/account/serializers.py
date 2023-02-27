""""
Serializers for Account
"""

from rest_framework import serializers
from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """ Serializer for Account Object """
    class Meta:
        model = Account
        fields = '__all__'
