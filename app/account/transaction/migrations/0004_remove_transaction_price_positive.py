# Generated by Django 3.2.18 on 2023-02-25 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_auto_20230225_0048'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='transaction',
            name='price_positive',
        ),
    ]
