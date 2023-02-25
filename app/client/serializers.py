from rest_framework import serializers

from client.models import Business, Account, Client


class BusinessSerializer(serializers.ModelSerializer):
    """ Serializer for the Business Object"""

    class Meta:
        model = Business
        fields = '__all__'
        extra_kwargs = {
            'code': {'required': True},
            'owner': {'required': True}
        }


class AccountSerializer(serializers.ModelSerializer):
    """ Serializer for Account Object """
    class Meta:
        model = Account
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    """ Serializer for Client Object """
    class Meta:
        model = Client
        fields = '__all__'
