# Generated by Django 3.2.18 on 2023-02-25 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_transaction_to_client_and_from_client_can_not_be_equal'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='transaction',
            name='to_client_and_from_client_can_not_be_equal',
        ),
    ]
