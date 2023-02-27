"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from account.transaction.models import Transaction
from django.db.utils import IntegrityError

from account.tests.factory import AccountFactory


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class ModelTransactionTests(TestCase):
    """Test models."""
    def setUp(self):
        """Create user and client."""
        self.account_1 = AccountFactory.create()
        self.account_2 = AccountFactory.create()

    def test_new_transaction(self):
        """Test creating a successful transaction."""
        value = 9999999.99
        transaction = Transaction()
        transaction.from_account = self.account_1
        transaction.to_account = self.account_2
        transaction.value = value
        transaction.save()

        self.assertEqual(transaction.value, value)

    def test_fail_new_transaction_with_negative_vale(self):
        """Test creating a fail transaction with a negative value."""
        value = -100
        transaction = Transaction()
        transaction.to_account = self.account_1
        transaction.from_account = self.account_2
        transaction.value = value

        with self.assertRaises(IntegrityError):
            transaction.save()

    def test_fail_new_transaction_with_value_0(self):
        """Test creating a fail transaction with value 0."""
        value = 0
        transaction = Transaction()
        transaction.to_account = self.account_1
        transaction.from_account = self.account_2
        transaction.value = value

        with self.assertRaises(IntegrityError):
            transaction.save()

    def test_fail_new_transaction_same_account(self):
        """Test creating a fail transaction with same client (from and to)."""
        value = 0
        transaction = Transaction()
        transaction.to_account = self.account_1
        transaction.from_account = self.account_2
        transaction.value = value

        with self.assertRaises(IntegrityError):
            transaction.save()

    def test_str_description(self):
        """ Test description of transaction"""
        Transaction()
        value = 10
        transaction = Transaction()
        transaction.to_account = self.account_1
        transaction.from_account = self.account_2
        transaction.value = value
        transaction.save()

        description_expected = \
            f"From Account: {transaction.from_account.number} | "\
            f"To Account: {transaction.to_account.number} | "\
            f"Value:  {transaction.value} | "\
            f"Type:  {transaction.get_type_display()}"

        self.assertEqual(
            str(transaction),
            description_expected
        )
