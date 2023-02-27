""""
URL mapping for the Transaction API
"""

from django.urls import path
from account.transaction import views

app_name = 'transaction'

urlpatterns = [
    path('create/', views.CreateTransactionView.as_view(), name='create'),
    path('list/', views.ListTransactionView.as_view(), name='list'),
]
