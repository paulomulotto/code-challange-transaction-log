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
        """Fail when create new account without client"""
        account = Account()
        account.client = ClientFactory.create()
        account.business = BusinessFactory.create()
        account.balance = -10000

        with self.assertRaises(IntegrityError):
            account.save()
