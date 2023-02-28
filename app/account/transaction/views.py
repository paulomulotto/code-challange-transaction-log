""""
Views for Transaction API
"""
from rest_framework import viewsets
from rest_framework import authentication, permissions
from django.db.models import Q
from .models import Transaction
from datetime import datetime
from rest_framework import mixins

from account.transaction.serializers import (
    TransactionSerializer
)


class TransactionViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet
        ):
    """
    A viewset that provides `retrieve`, `create`, and `list`
    actions from Transactions.
    """
    serializer_class = TransactionSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def apply_date_filter(self, queryset, start_date_str, end_date_str):
        """" Apply date range filter if necessary """
        if start_date_str is not None and end_date_str is not None:
            start_date = datetime.strptime(
                start_date_str, '%Y/%m/%d %H:%M:%S.%f')
            end_date = datetime.strptime(
                end_date_str, '%Y/%m/%d %H:%M:%S.%f')
            date_filter = Q(
                created_at__gte=start_date, created_at__lte=end_date)
            queryset = queryset.filter(date_filter)
        return queryset

    def apply_type_filter(self, queryset, transaction_type=None):
        """ Apply type transaction filter if necessary"""
        if transaction_type is not None:
            queryset = queryset.filter(type=transaction_type)
        return queryset

    def apply_business_filter(self, queryset, business_id=None):
        """ Apply Business filter if necessary"""
        if business_id is not None:
            queryset = queryset.filter(to_account__business=business_id)
        return queryset

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(
            Q(from_account__client__user=user) |
            Q(to_account__client__user=user)
        )

        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')
        queryset = self.apply_date_filter(
            queryset, start_date_str, end_date_str)

        transaction_type = self.request.query_params.get('transaction_type')
        queryset = self.apply_type_filter(queryset, transaction_type)

        business_id = self.request.query_params.get('business_id')
        queryset = self.apply_business_filter(queryset, business_id)

        return queryset
