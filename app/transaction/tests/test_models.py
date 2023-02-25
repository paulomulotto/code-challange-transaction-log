"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from transaction.models import Transaction
from django.db.utils import IntegrityError


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class ModelTests(TestCase):
    """Test models."""
    def setUp(self):
        """Create user and client."""
        self.user_1 = create_user(
            email='user_1@example.com',
            password='testpass123',
            name='User 1 Name',
        )
        self.user_2 = create_user(
            email='user_2@example.com',
            password='testpass123',
            name='User 2 Name',
        )

    def test_new_transaction(self):
        """Test creating a successful transaction."""
        value = 9999999.99
        transaction = Transaction()
        transaction.from_client = self.user_1
        transaction.to_client = self.user_2
        transaction.value = value
        transaction.save()

        self.assertEqual(transaction.value, value)

    def test_fail_new_transaction_with_negative_vale(self):
        """Test creating a fail transaction with a negative value."""
        value = -100
        transaction = Transaction()
        transaction.to_client = self.user_1
        transaction.from_client = self.user_2
        transaction.value = value

        with self.assertRaises(IntegrityError):
            transaction.save()

    def test_fail_new_transaction_with_value_0(self):
        """Test creating a fail transaction with value 0."""
        value = 0
        transaction = Transaction()
        transaction.to_client = self.user_1
        transaction.from_client = self.user_2
        transaction.value = value

        with self.assertRaises(IntegrityError):
            transaction.save()

    def test_fail_new_transaction_same_client(self):
        """Test creating a fail transaction with same client (from and to)."""
        value = 0
        transaction = Transaction()
        transaction.to_client = self.user_1
        transaction.from_client = self.user_1
        transaction.value = value

        with self.assertRaises(IntegrityError):
            transaction.save()
