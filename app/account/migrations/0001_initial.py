# Generated by Django 3.2.18 on 2023-02-27 19:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0011_account_balance_positive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('number', models.BigAutoField(primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_active', models.BooleanField(default=True)),
                ('business', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.business')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='client.client')),
            ],
        ),
        migrations.AddConstraint(
            model_name='account',
            constraint=models.CheckConstraint(check=models.Q(('balance__gt', 0)), name='balance_positive'),
        ),
    ]
