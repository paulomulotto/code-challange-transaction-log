from rest_framework import generics
from client.models import Business, Account
from client.serializers import (
        BusinessSerializer,
        AccountSerializer,
        ClientSerializer,
    )


class CreateBusinessView(generics.CreateAPIView):
    """ Create a new business """
    serializer_class = BusinessSerializer


class UpdateBusinessView(generics.UpdateAPIView):
    """ Update a business """
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()


class CreateAccountView(generics.CreateAPIView):
    serializer_class = AccountSerializer


class CreateClientView(generics.CreateAPIView):
    serializer_class = ClientSerializer


class UpdateClientView(generics.UpdateAPIView):
    """ Update a client """
    serializer_class = ClientSerializer
    queryset = Account.objects.all()