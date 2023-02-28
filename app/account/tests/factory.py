""""
Factory for building account objects used in tests
"""
from core.tests.object_factory import ObjectFactory

from account.models import Account
from client.tests.factory import ClientFactory, BusinessFactory


class AccountFactory(ObjectFactory):
    @classmethod
    def create(cls, client=None, business=None, balance=None,
               with_business=True):

        if business and not with_business:
            raise Exception(
                "To create an account with business "
                "with_business should be True"
            )

        account = Account()
        account.client = client or ClientFactory.create()
        if with_business:
            account.business = business or BusinessFactory.create()
        account.balance = balance or 10000
        account.save()
        return account
