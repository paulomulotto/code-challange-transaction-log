""""
Factory for building account objects used in tests
"""
from core.tests.object_factory import ObjectFactory

from account.models import Account
from client.tests.factory import ClientFactory, BusinessFactory


class AccountFactory(ObjectFactory):
    @classmethod
    def create(cls, client=None, business=None, balance=None):
        account = Account()
        account.client = client or ClientFactory.create()
        account.bussiness = business or BusinessFactory.create()
        account.balance = balance or 10000
        account.save()
        return account
