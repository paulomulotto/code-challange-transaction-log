from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import constraints, Q


class Client(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    company = models.ForeignKey(
        "Business",
        on_delete=models.SET_NULL,
        blank=True, null=True,
        default=None
    )


class Account(models.Model):
    number = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    #  9,999,999,999,999.99
    balance = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    business = models.ForeignKey(
        "Business",
        on_delete=models.SET_NULL,
        blank=True, null=True,
        default=None
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            constraints.CheckConstraint(
                check=Q(balance__gt=0),
                name='balance_positive'
            )
        ]


class Business(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=15,
        unique=True,
        blank=False,
        default=None
    )
    owner = models.ForeignKey(Client, on_delete=models.PROTECT)
