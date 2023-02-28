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

    def filter_date_range(self, queryset):
        """" Apply date range filter if necessary """
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        if start_date_str is not None and end_date_str is not None:
            start_date = datetime.strptime(
                start_date_str, '%Y/%m/%d %H:%M:%S.%f')
            end_date = datetime.strptime(
                end_date_str, '%Y/%m/%d %H:%M:%S.%f')
            date_filter = Q(
                created_at__gte=start_date, created_at__lte=end_date)
            queryset = queryset.filter(date_filter)
        return queryset

    def filter_transaction_type(self, queryset):
        """ Apply type transaction filter if necessary"""
        transaction_type = self.request.query_params.get('transaction_type')
        if transaction_type is not None:
            queryset = queryset.filter(type=transaction_type)
        return queryset

    def filter_owner_user(self, queryset):
        """ Apply user filter.
            * Should always exists an users as auth is mandatory
            to access this function
        """
        user = self.request.user
        queryset = queryset.filter(
            Q(from_account__client__user=user) |
            Q(to_account__client__user=user)
        )
        return queryset

    def filter_business_id(self, queryset):
        """ Apply business filter if necessary"""
        business_id = self.request.query_params.get('business_id')
        if business_id is not None:
            queryset = queryset.filter(to_account__business=business_id)
        return queryset

    def apply_custom_filters(self, queryset):
        """ Build all filters """
        for name_attr in dir(self):
            if name_attr.startswith('filter_'):
                attr = getattr(self, name_attr)
                if callable(attr):
                    filter_function = attr
                    queryset = filter_function(queryset)
        return queryset

    def get_queryset(self):
        """Get the query set for transactions"""
        queryset = Transaction.objects.all()
        queryset = self.apply_custom_filters(queryset)
        return queryset
