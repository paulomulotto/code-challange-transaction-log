""""
Test for the Transaction API
"""
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from account.tests.factory import AccountFactory
from account.transaction.models import Transaction

from rest_framework.test import APIClient
from rest_framework import status

CREATE_TRANSACTION_URL = reverse('transaction:transaction-list')
GET_TRANSACTION_URL = 'transaction:transaction-detail'
LIST_TRANSACTION_URL = reverse('transaction:transaction-list')

DATETIME_FMT = '%Y/%m/%d %H:%M:%S.%f'


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
        self.api_client.force_authenticate(self.to_account.client.user)
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
        self.api_client.force_authenticate(self.from_account.client.user)

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
        self.api_client.force_authenticate(self.from_account.client.user)
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
        self.api_client.force_authenticate(self.from_account.client.user)
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
        self.api_client.force_authenticate(self.from_account.client.user)
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
        self.api_client.force_authenticate(self.from_3_account.client.user)
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
        self.api_client.force_authenticate(self.from_account.client.user)
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

    def test_filter_transaction_date(self):
        """Test filter transaction by date"""
        # User 1
        self.api_client.force_authenticate(self.from_account.client.user)
        value = 10
        payload = {
            'from_account': self.from_account.number,
            'to_account': self.to_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }
        time_0 = timezone.now()
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        time_1 = timezone.now()
        id_transaction_1 = res.data['id']

        payload['value'] = 30
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        id_transaction_2 = res.data['id']

        value = 20
        payload = {
            'from_account': self.from_account.number,
            'to_account': self.to_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }
        time_2 = timezone.now()
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        id_transaction_3 = res.data['id']
        time_3 = timezone.now()

        # Time 0 -> 1
        res = self.api_client.get(
            f'{LIST_TRANSACTION_URL}'
            f'?start_date={time_0.strftime(DATETIME_FMT)}'
            f'&end_date={time_1.strftime(DATETIME_FMT)}'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transactions_in_system = []
        for transaction in res.data:
            transactions_in_system.append(transaction['id'])
        self.assertListEqual(
            [id_transaction_1], transactions_in_system)

        # Time 1 -> 2
        res = self.api_client.get(
            f'{LIST_TRANSACTION_URL}'
            f'?start_date={time_1.strftime(DATETIME_FMT)}'
            f'&end_date={time_2.strftime(DATETIME_FMT)}'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transactions_in_system = []
        for transaction in res.data:
            transactions_in_system.append(transaction['id'])
        self.assertListEqual(
            [id_transaction_2], transactions_in_system)

        # Time 0 -> 3
        res = self.api_client.get(
            f'{LIST_TRANSACTION_URL}'
            f'?start_date={time_0.strftime(DATETIME_FMT)}'
            f'&end_date={time_3.strftime(DATETIME_FMT)}'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transactions_in_system = []
        for transaction in res.data:
            transactions_in_system.append(transaction['id'])
        self.assertListEqual(
            [id_transaction_1, id_transaction_2, id_transaction_3],
            transactions_in_system)

    def test_transaction_filter_type(self):
        """ Test transaction type filter """
        main_account = self.from_account
        self.api_client.force_authenticate(main_account.client.user)
        value = 10
        transaction_type = Transaction.EXPENSES
        payload = {
            'from_account': main_account.number,
            'to_account': self.to_account.number,
            'value': value,
            'type': transaction_type
        }
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        id_transaction_1 = res.data['id']

        transaction_type = Transaction.DEPOSITS
        payload = {
            'to_account': main_account.number,
            'value': value,
            'type': transaction_type
        }
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        id_transaction_2 = res.data['id']

        transaction_type = Transaction.WITHDRAWALS
        payload = {
            'from_account': main_account.number,
            'value': value,
            'type': transaction_type
        }
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        id_transaction_3 = res.data['id']

        # Type 1
        res = self.api_client.get(
            f'{LIST_TRANSACTION_URL}'
            f'?transaction_type={Transaction.EXPENSES}'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transactions_returned = []
        for transaction in res.data:
            transactions_returned.append(transaction['id'])
        self.assertListEqual(
            [id_transaction_1], transactions_returned)

        # Type 2
        res = self.api_client.get(
            f'{LIST_TRANSACTION_URL}'
            f'?transaction_type={Transaction.DEPOSITS}'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transactions_returned = []
        for transaction in res.data:
            transactions_returned.append(transaction['id'])
        self.assertListEqual(
            [id_transaction_2], transactions_returned)

        # Type 3
        res = self.api_client.get(
            f'{LIST_TRANSACTION_URL}'
            f'?transaction_type={Transaction.WITHDRAWALS}'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transactions_returned = []
        for transaction in res.data:
            transactions_returned.append(transaction['id'])
        self.assertListEqual(
            [id_transaction_3], transactions_returned)

        # All Transactions - > Without Filter
        res = self.api_client.get(LIST_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transactions_returned = []
        for transaction in res.data:
            transactions_returned.append(transaction['id'])
        self.assertListEqual(
            [id_transaction_1, id_transaction_2, id_transaction_3], transactions_returned)

    def test_restrict_access_transactions(self):
        """ Test that users can see only their own transactions """
        # User 1

        self.api_client.force_authenticate(self.from_account.client.user)
        value = 10
        payload = {
            'from_account': self.from_account.number,
            'to_account': self.to_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        id_transaction_1 = res.data['id']

        # User 2
        self.api_client.force_authenticate(self.from_3_account.client.user)
        value = 20
        payload = {
            'from_account': self.from_3_account.number,
            'to_account': self.to_4_account.number,
            'value': value,
            'type': Transaction.EXPENSES
        }
        res = self.api_client.post(CREATE_TRANSACTION_URL, payload)
        id_transaction_2 = res.data['id']

        # User 2
        # Attempt to access another user's transaction
        res = self.api_client.get(
            reverse(GET_TRANSACTION_URL, args=[id_transaction_1]))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Attempt to access their own transaction
        res = self.api_client.get(
            reverse(GET_TRANSACTION_URL, args=[id_transaction_2]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # User 1
        self.api_client.force_authenticate(self.from_account.client.user)
        # Attempt to access another user's transaction
        res = self.api_client.get(
            reverse(GET_TRANSACTION_URL, args=[id_transaction_2]))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Attempt to access their own transaction
        res = self.api_client.get(
            reverse(GET_TRANSACTION_URL, args=[id_transaction_1]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
