""""
URL mapping for account app
"""
from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('account/', views.CreateAccountView.as_view(), name='create-account'),
    path('account/balance/', views.BalanceView.as_view(), name='balance'),
]
