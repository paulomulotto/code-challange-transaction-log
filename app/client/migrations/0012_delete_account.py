# Generated by Django 3.2.18 on 2023-02-27 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0014_auto_20230227_1904'),
        ('client', '0011_account_balance_positive'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
