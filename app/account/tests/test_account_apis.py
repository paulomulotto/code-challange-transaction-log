""""
Test for the account APIs
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient
from account.tests.factory import AccountFactory

from client.tests.factory import ClientFactory, BusinessFactory


CREATE_ACCOUNT_URL = "account:create-account"
GET_BALANCE_URL = "account:balance"


class AccountApiTests(TestCase):
    """ Tests for Account APIs"""

    def setUp(self):
        """ Set up data used in tests """
        self.api_client = APIClient()
        self.client = ClientFactory.create()
        self.business = BusinessFactory.create()

    def test_sucessful_creating_account(self):
        """ Successful test of creating account """
        payload = dict(
            client=self.client.id,
            business=self.business.id,
            balance=1000
        )
        res = self.api_client.post(reverse(CREATE_ACCOUNT_URL), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_sucessful_creating_account_without_business(self):
        """ Successful test of creating account without business"""
        payload = dict(
            client=self.client.id,
            balance=1000
        )
        res = self.api_client.post(reverse(CREATE_ACCOUNT_URL), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_fail_creating_account_without_client(self):
        """ Failure to create an account without client """
        payload = dict(
            business=self.business
        )
        res = self.api_client.post(reverse(CREATE_ACCOUNT_URL), payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_creating_account_negative_balance(self):
        """ Successful test of creating account """
        payload = dict(
            client=self.client.id,
            business=self.business.id,
            balance=-100
        )
        res = self.api_client.post(reverse(CREATE_ACCOUNT_URL), payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_balance_with_business(self):
        """ Test get balance of an Business Account user"""
        balance = 900
        account = AccountFactory.create(client=self.client, balance=balance)

        self.api_client.force_authenticate(user=account.client.user)

        url = f'{reverse(GET_BALANCE_URL)}?business_id={account.business.pk}'
        res = self.api_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['balance'], balance)

    def test_get_balance_without_business(self):
        """ Test get balance of an Account user"""
        balance = 900
        account = AccountFactory.create(
            client=self.client, balance=balance, with_business=False)

        self.api_client.force_authenticate(user=account.client.user)

        url = reverse(GET_BALANCE_URL)
        res = self.api_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['balance'], balance)
