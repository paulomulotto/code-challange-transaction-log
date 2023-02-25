""""
Test for models of client
"""
from django.test import TestCase
from user.tests.factory import UserFactory
from client.models import Client, Account, Business
from client.tests.factory import ClientFactory, BusinessFactory
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

    def test_successfull_new_client_without_company(self):
        """ Test creating a successful client without company"""
        client = Client()
        client.user = self.user_1
        client.save()


class AccountModelTests(TestCase):

    def setUp(self):
        """Create user."""
        self.user_1 = UserFactory.create()

    def test_successfull_new_account_without_company(self):
        """Create new account without a business"""
        account = Account()
        account.client = ClientFactory.create()
        account.save()
        self.assertGreaterEqual(account.number, 1)

    def test_successfull_new_account_with_company(self):
        """Create new account with related to a business"""
        account = Account()
        account.client = ClientFactory.create()
        account.business = BusinessFactory.create()
        account.save()
        self.assertGreaterEqual(account.number, 1)

    def test_fail_new_account_without_client(self):
        """Fail when create new account without client"""
        account = Account()
        with self.assertRaises(IntegrityError):
            account.save()


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
