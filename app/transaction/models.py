from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import Q, F, constraints

class Transaction(models.Model):
    from_client = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='from_client')
    to_client = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='to_client')
    value = models.DecimalField(max_digits=9, decimal_places=2,  validators=[MinValueValidator(0)]) #9,999,999.99


    class Meta:
        constraints = [
            constraints.CheckConstraint(
                check=Q(value__gt=0),
                name='value_positive'
            ),
            constraints.CheckConstraint(
                check=~Q(from_client=F('to_client')),
                name='to_client_and_from_client_can_not_be_equal'
            ),
        ]