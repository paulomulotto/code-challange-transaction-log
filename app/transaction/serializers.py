""""
Serializers for the Transaction View.
"""
from rest_framework import serializers
from transaction.models import Transaction
from django.utils.translation import gettext as _
from django.db import IntegrityError, transaction

from client.models import Account


class TransactionSerializer(serializers.ModelSerializer):
    """ Serializer for the transaction object. """

    class Meta:
        model = Transaction
        fields = '__all__'
        # extra_kwargs = {
        #     'from_account': {
        #         "required": False
        #     },
        #     'to_account': {
        #         "required": False
        #     }
        # }

    def transaction_commit(self, validated_data):
        try:
            with transaction.atomic():
                value = validated_data['value']

                if self.validated_data['type'] == Transaction.DEPOSITS:
                    to_account = Account.objects.get(
                        number=validated_data['to_account'].number
                    )
                    to_account.balance = to_account.balance + value
                    to_account.save()

                elif self.validated_data['type'] == Transaction.WITHDRAWALS:
                    from_account = Account.objects.get(
                        number=validated_data['from_account'].number
                    )
                    from_account.balance = from_account.balance - value
                    from_account.save()

                elif self.validated_data['type'] == Transaction.EXPENSES:
                    to_account = Account.objects.get(
                        number=validated_data['to_account'].number
                    )
                    to_account.balance = to_account.balance + value
                    to_account.save()

                    from_account = Account.objects.get(
                        number=validated_data['from_account'].number
                    )
                    from_account.balance = from_account.balance - value
                    from_account.save()

        except IntegrityError:
            msg = _('Unable to complete the transaction. Negative balance.')
            raise serializers.ValidationError(msg, code='negative_balance')

    def create(self, validated_data):
        """ Create and return a transaction if it is valid."""
        self.transaction_commit(validated_data)
        return Transaction.objects.create(**validated_data)
