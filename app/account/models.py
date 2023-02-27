from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import constraints, Q
from client.models import Client, Business


class Account(models.Model):
    number = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    #  9,999,999,999,999.99
    balance = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        default=None
    )

    class Meta:
        constraints = [
            constraints.CheckConstraint(
                check=Q(balance__gt=0),
                name='balance_positive'
            ),
            models.UniqueConstraint(
                fields=['client', 'business'], name="unique_client_business"),
            models.UniqueConstraint(
                fields=['client'],
                condition=Q(business=None),
                name="unique_client"),
        ]
