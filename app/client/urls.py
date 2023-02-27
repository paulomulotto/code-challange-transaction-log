""""
URL mappings for the client API
"""
from django.urls import path
from client import views

app_name = 'client'

urlpatterns = [
    path('business/<int:pk>/', views.UpdateBusinessView.as_view(), name='update-business'),
    path('business/', views.CreateBusinessView.as_view(), name='create-business'),
    path('client/', views.CreateClientView.as_view(), name='create-client'),
    path('client/<int:pk>/', views.UpdateClientView.as_view(), name='update-client'),
]
