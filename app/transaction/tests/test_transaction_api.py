""""
Test for the Transaction API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from user.tests.factory import UserFactory
from transaction.models import Transaction

from rest_framework.test import APIClient
from rest_framework import status

CREATE_TRANSACTION_URL = reverse('transaction:create')

class TransactionApiTests(TestCase):
    """Test Transaction API """
    def setUp(self):
        """Create user and client."""
        self.user_1 = UserFactory.create(
            email='user_1@example.com',
            password='testpass123',
            name='User 1 Name',
        )
        self.user_2 = UserFactory.create(
            email='user_2@example.com',
            password='testpass123',
            name='User 2 Name',
        )
        self.client = APIClient()

    def test_successfull_transaction(self):
        """ Test creating a successful transacion"""
        payload = {
            'from_client': self.user_1.id,
            'to_client': self.user_2.id,
            'value': 100,
        }
        res = self.client.post(CREATE_TRANSACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        transaction_exists = Transaction.objects.filter(
            from_client=self.user_1.id,
            to_client=self.user_2.id,
        )

