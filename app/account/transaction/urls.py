""""
URL mapping for the Transaction API
"""
from django.urls import path
from account.transaction import views
from rest_framework.routers import DefaultRouter

app_name = 'transaction'

router = DefaultRouter()
router.register(r'', views.TransactionViewSet, basename='transaction')

urlpatterns = router.urls
