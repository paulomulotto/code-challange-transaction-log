""""
Tests for Account Models
"""
from django.test import TestCase
from user.tests.factory import UserFactory
from account.models import Account
from client.tests.factory import ClientFactory, BusinessFactory
from django.db.utils import IntegrityError


class AccountModelTests(TestCase):

    def setUp(self):
        """Create user."""
        self.user_1 = UserFactory.create()

    def test_successful_new_account_without_company(self):
        """Create new account without a business"""
        account = Account()
        account.client = ClientFactory.create()
        account.balance = 10000
        account.save()
        self.assertGreaterEqual(account.number, 1)

    def test_successful_new_account_with_company(self):
        """Create new account with related to a business"""
        account = Account()
        account.client = ClientFactory.create()
        account.business = BusinessFactory.create()
        account.balance = 10000
        account.save()
        self.assertGreaterEqual(account.number, 1)

    def test_fail_new_account_without_client(self):
        """Fail when create new account without client"""
        account = Account()
        with self.assertRaises(IntegrityError):
            account.save()

    def test_fail_new_account_negative_balance(self):
        """Fail when create new account with negative balance"""
        account = Account()
        account.client = ClientFactory.create()
        account.business = BusinessFactory.create()
        account.balance = -10000

        with self.assertRaises(IntegrityError):
            account.save()

    def test_fail_more_than_one_account_same_client_without_business(self):
        """Fail when create new account for the same
        client without business """
        account = Account()
        account.client = ClientFactory.create()
        account.balance = 100
        account.save()

        account_2 = Account()
        account_2.client = account.client
        account_2.balance = 150

        with self.assertRaises(IntegrityError):
            account_2.save()

    def test_fail_more_than_one_account_same_client_same_business(self):
        """Fail when create new account for the same and
        client same business """
        account = Account()
        account.client = ClientFactory.create()
        account.business = BusinessFactory.create()
        account.balance = 100
        account.save()

        account_2 = Account()
        account_2.client = account.client
        account_2.business = account.business
        account_2.balance = 150

        with self.assertRaises(IntegrityError):
            account_2.save()

    def test_success_more_than_one_account_diff_business(self):
        """Success when create new account for the same
        client with diff business"""
        account = Account()
        account.client = ClientFactory.create()
        account.balance = 100
        account.save()

        account_2 = Account()
        account_2.client = account.client
        account_2.business = BusinessFactory.create()
        account_2.balance = 150
        account_2.save()

        account_3 = Account()
        account_3.client = account.client
        account_3.business = BusinessFactory.create()
        account_3.balance = 150
        account_3.save()

    def test_str_description(self):
        """ Test description of transaction"""
        account = Account()
        account.client = ClientFactory.create()
        account.balance = 100
        account.save()
        self.assertEqual(
            str(account),
            f'{account.number}'
        )
