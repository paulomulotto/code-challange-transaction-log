""""
Database models for Clients
"""
from django.db import models
from django.contrib.auth import get_user_model


class Client(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    company = models.ForeignKey(
        "Business",
        on_delete=models.SET_NULL,
        blank=True, null=True,
        default=None
    )


class Business(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=15,
        unique=True,
        blank=False,
        default=None
    )
    owner = models.ForeignKey(Client, on_delete=models.PROTECT)
