""""
Test for models of client
"""
from django.test import TestCase
from user.tests.factory import UserFactory
from client.models import Client, Business
from client.tests.factory import ClientFactory
from django.db.utils import IntegrityError


class ClientModelTests(TestCase):
    """Test Transaction API """
    def setUp(self):
        """Create users."""
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

    def test_successful_new_client_without_company(self):
        """ Test creating a successful client without company"""
        client = Client()
        client.user = self.user_1
        client.save()


class BusinessModelTests(TestCase):

    def test_sucessfull_new_business(self):
        """Test creating a succesfull Business """
        business = Business()
        business.name = "new business"
        business.code = "1234-5677"
        business.owner = ClientFactory.create()
        business.save()

    def test_fail_business_without_code(self):
        """Test creating a invalid Business without code """
        business = Business()
        business.name = "new business"

        with self.assertRaises(IntegrityError):
            business.save()

    def test_fail_business_without_owner(self):
        """Test creating a invalid Business without owner """
        business = Business()
        business.name = "new business"
        business.code = "1234-5677"

        with self.assertRaises(IntegrityError):
            business.save()
