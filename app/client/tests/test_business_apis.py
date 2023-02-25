""""
Tests for the Clients API
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from client.tests.factory import ClientFactory
from client.models import Business

CREATE_BUSINESS_URL = reverse('client:create-business')
UPDATE_BUSINESS_URL = 'client:update-business'


class BusinessApiTests(TestCase):
    """ Tests for the Business API"""
    def setUp(self):
        self.api_client = APIClient()

        self.client = ClientFactory.create()

    def test_successful_creating_business(self):
        """ Successful test of creating business """
        name = "Test Name"
        code = "1234-1234"
        payload = {
            "name": name,
            "code": code,
            "owner": self.client.id
        }
        res = self.api_client.post(CREATE_BUSINESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        business = Business.objects.get(code=code)
        self.assertEqual(business.name, name)
        self.assertEqual(res.data['id'], business.id)

    def test_fail_creating_business_without_code(self):
        """ Failure to create an ownerless business without code """
        name = "Test Name"
        payload = {
            "name": name,
            "owner": self.client.id
        }
        res = self.api_client.post(CREATE_BUSINESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_creating_business_without_owner(self):
        """ Failure to create an ownerless business without owner """
        name = "Test Name"
        code = "1234-1234"
        payload = {
            "name": name,
            "code": code,
        }
        res = self.api_client.post(CREATE_BUSINESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_creating_business_without_name(self):
        """ Failure to create an ownerless business without name """
        code = "1234-1234"
        payload = {
            "code": code,
            "owner": self.client.id
        }
        res = self.api_client.post(CREATE_BUSINESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_update_business_with_put(self):
        """ Success to update a business name """
        name = "Test Name"
        code = "1234-1234"
        payload = {
            "name": name,
            "code": code,
            "owner": self.client.id
        }
        res = self.api_client.post(CREATE_BUSINESS_URL, payload)

        new_name = "Test New Name"
        payload['name'] = new_name
        res = self.api_client.put(
            reverse(f'{UPDATE_BUSINESS_URL}', kwargs={'pk': res.data["id"]}),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        business = Business.objects.get(code=code)
        self.assertEqual(business.name, new_name)

    def test_successful_update_business_with_patch(self):
        """ Success to update a business name """
        name = "Test Name"
        code = "1234-1234"
        payload = {
            "name": name,
            "code": code,
            "owner": self.client.id
        }
        res = self.api_client.post(CREATE_BUSINESS_URL, payload)

        new_name = "Test New Name"
        res = self.api_client.patch(
            reverse(f'{UPDATE_BUSINESS_URL}', kwargs={'pk': res.data["id"]}),
            {"name": new_name}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        business = Business.objects.get(code=code)
        self.assertEqual(business.name, new_name)
