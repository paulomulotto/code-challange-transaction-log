""""
Test for the Client APIs
"""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from client.tests.factory import BusinessFactory
from user.tests.factory import UserFactory

CREATE_CLIENT_URL = reverse('client:create-client')


class ClientApiTests(TestCase):
    """ Tests for Client APIs """

    def setUp(self):
        """ Set up data used in tests """
        self.api_client = APIClient()
        self.business = BusinessFactory.create()
        self.user = UserFactory.create()

    def test_successful_create_client(self):
        """ Success in creating customer with company """
        payload = dict(
            user=self.user.id,
            company=self.business.id
        )
        res = self.api_client.post(CREATE_CLIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_successful_create_client_without_company(self):
        """ Success in creating customer without company """
        payload = dict(
            user=self.user.id,
        )
        res = self.api_client.post(CREATE_CLIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_fail_create_client_without_user(self):
        """ Failure to create an client without user """
        payload = dict(
            company=self.business.id
        )
        res = self.api_client.post(CREATE_CLIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
