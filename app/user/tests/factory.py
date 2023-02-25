from core.tests.object_factory import ObjectFactory
from django.contrib.auth import get_user_model

class UserFactory(ObjectFactory):
    @classmethod
    def create(cls, email='user@example.com', password='testpass123', **params):
        """Create and return a new user."""
        return get_user_model().objects.create_user(email, password, **params)