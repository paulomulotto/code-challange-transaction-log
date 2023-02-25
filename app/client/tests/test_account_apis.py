""""
Test for the account APIs
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from client.tests.factory import ClientFactory, BusinessFactory


CREATE_ACCOUNT_URL = "client:create-account"


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
            business=self.business.id
        )
        res = self.api_client.post(reverse(CREATE_ACCOUNT_URL), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_sucessful_creating_account_without_business(self):
        """ Successful test of creating account without business"""
        payload = dict(
            client=self.client.id,
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
