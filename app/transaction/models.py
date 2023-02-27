from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q, F, constraints
from client.models import Account


class Transaction(models.Model):
    DEPOSITS = 'DP'
    WITHDRAWALS = 'WD'
    EXPENSES = 'EX'
    TYPES = [
        (DEPOSITS, 'Deposits'),
        (WITHDRAWALS, 'Withdrawals'),
        (EXPENSES, 'Expenses'),

    ]

    from_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='from_account',
        blank=True, null=True
    )
    to_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='to_account',
        blank=True, null=True
    )
    value = models.DecimalField(
        max_digits=9, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    type = models.CharField(
        max_length=2,
        choices=TYPES,
        default=EXPENSES,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        description = \
            f"From Account: {self.from_account.number} | "\
            f"To Account: {self.to_account.number} | "\
            f"Value:  {self.value} | "\
            f"Type:  {self.get_type_display()}"

        return description

    class Meta:
        constraints = [
            constraints.CheckConstraint(
                check=Q(value__gt=0),
                name='value_positive'
            ),
            constraints.CheckConstraint(
                check=~Q(from_account=F('to_account')),
                name='to_account_and_from_account_can_not_be_equal'
            ),
            constraints.CheckConstraint(
                check=Q(from_account__isnull=False) |
                Q(to_account__isnull=False),
                name='at_leat_one_of_to_account_or_from_account_must_be_fill'
            ),
        ]
        ordering = ('created_at', )
