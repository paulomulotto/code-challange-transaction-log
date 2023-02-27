""""
Test for the Transaction API
"""
from django.test import TestCase
from django.urls import reverse
from account.tests.factory import AccountFactory
from account.transaction.models import Transaction

from rest_framework.test import APIClient
from rest_framework import status

CREATE_TRANSACTION_URL = reverse('transaction:create')
# GET_TRANSACTION_URL = reverse('transaction:get')
LIST_TRANSACTION_URL = reverse('transaction:list')


class TransactionApiTests(TestCase):
    """Test Transaction API """
    def setUp(self):
        """Create user and client."""
        self.from_account = AccountFactory.create()
        self.to_account = AccountFactory.create()

        self.from_3_account = AccountFactory.create()
        self.to_4_account = AccountFactory.create()

        self.api_client = APIClient()

    def test_successful_transaction_deposit(self):
        """ Test creating a successful transacion deposit type"""
        value = 100
        payload = {
            'to_account': self.to_account.number,
            'value': value,
            'type': Transaction.DEPOSITS
        }

        old_balance_to_account = self.to_account.balance
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        transaction_exists = Transaction.objects.filter(
            to_account=self.to_account.number,
        ).exists()
        self.assertTrue(transaction_exists)

        self.to_account.refresh_from_db()

        self.assertEqual(
            old_balance_to_account + value, self.to_account.balance
            )

    def test_successful_transaction_withdrawals(self):
        """ Test creating a successful transacion WITHDRAWALS type"""
        value = 100
        payload = {
            'from_account': self.from_account.number,
            'value': value,
            'type': Transaction.WITHDRAWALS
        }

        old_balance_from_account = self.from_account.balance
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        transaction_exists = Transaction.objects.filter(
            from_account=self.from_account.number,
        ).exists()
        self.assertTrue(transaction_exists)

        self.from_account.refresh_from_db()

        self.assertEqual(
            old_balance_from_account - value, self.from_account.balance
            )

    def test_successful_transaction(self):
        """ Test creating a successful transacion"""
        value = 100
        payload = {
            'from_account': self.from_account.number,
            'to_account': self.to_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }

        old_balance_from_account = self.from_account.balance
        old_balance_to_account = self.to_account.balance
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        transaction_exists = Transaction.objects.filter(
            from_account=self.from_account.number,
            to_account=self.to_account.number,
        ).exists()
        self.assertTrue(transaction_exists)

        self.from_account.refresh_from_db()
        self.to_account.refresh_from_db()

        self.assertEqual(
            old_balance_from_account - value, self.from_account.balance
            )
        self.assertEqual(
            old_balance_to_account + value, self.to_account.balance
            )

    def test_fail_transaction_negative_balance(self):
        """ Fail when create a transaction that let a account in
            negative balance.
            The balance should remain the same
        """
        value = 10000000
        payload = {
            'from_account': self.from_account.number,
            'to_account': self.to_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }

        old_balance_from_account = self.from_account.balance
        old_balance_to_account = self.to_account.balance
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        transaction_exists = Transaction.objects.filter(
            from_account=self.from_account.number,
            to_account=self.to_account.number,
        ).exists()
        self.assertFalse(transaction_exists)

        self.from_account.refresh_from_db()
        self.to_account.refresh_from_db()

        self.assertEqual(old_balance_from_account, self.from_account.balance)
        self.assertEqual(old_balance_to_account, self.to_account.balance)

    def test_succesful_get_transactions(self):
        """ Retrive transactions """
        # User 1
        self.api_client.force_login(self.from_account.client.user)
        value = 10
        payload = {
            'from_account': self.from_account.number,
            'to_account': self.to_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        payload['value'] = 30
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)

        res = self.api_client.get(LIST_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for transaction in res.data:
            self.assertEqual(
                transaction['from_account'], self.from_account.pk)

        # User 2
        self.api_client.force_login(self.from_3_account.client.user)
        value = 20
        payload = {
            'from_account': self.from_3_account.number,
            'to_account': self.to_4_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)

        res = self.api_client.get(LIST_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for transaction in res.data:
            self.assertEqual(
                transaction['from_account'], self.from_3_account.pk)

    def test_order_transactions(self):
        """ Validate default order in transactions """
        # User 1
        self.api_client.force_login(self.from_account.client.user)
        value = 10
        payload = {
            'from_account': self.from_account.number,
            'to_account': self.to_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        id_transaction_1 = res.data['id']

        payload['value'] = 30
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        id_transaction_2 = res.data['id']

        # User 3
        self.api_client.force_login(self.from_3_account.client.user)
        value = 20
        payload = {
            'from_account': self.from_3_account.number,
            'to_account': self.to_4_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)

        # User 1
        self.api_client.force_login(self.from_account.client.user)
        res = self.api_client.get(LIST_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        transactions_in_system = []
        for transaction in res.data:
            transactions_in_system.append(transaction['id'])
        self.assertListEqual(
            [id_transaction_1, id_transaction_2], transactions_in_system)
