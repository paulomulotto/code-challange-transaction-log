from core.tests.object_factory import ObjectFactory
from user.tests.factory import UserFactory
from client.models import Client, Business

import random


class ClientFactory(ObjectFactory):
    @classmethod
    def create(cls, email=None, name=None, password=None, **paramns):
        user_1 = UserFactory.create(
            email=email or f'user_{random.randint(100, 99999)}@example.com',
            password=password or 'testpass123',
            name=name or f'User {random.randint(100, 99999)} Name',
        )
        client = Client()
        client.user = user_1
        client.save()
        return client


class BusinessFactory(ObjectFactory):
    @classmethod
    def create(cls, name=None, code=None, owner=None, **paramns):
        business = Business()
        business.name = name or f"new business {random.randint(100, 99999)}"
        business.code = code or f"1234-5677-{random.randint(100, 99999)}"
        business.owner = owner or ClientFactory.create()
        business.save()
        return business
