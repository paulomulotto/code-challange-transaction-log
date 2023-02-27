# Generated by Django 3.2.18 on 2023-02-27 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20230227_2014'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='account',
            constraint=models.UniqueConstraint(fields=('client', 'business'), name='unique_client_business'),
        ),
        migrations.AddConstraint(
            model_name='account',
            constraint=models.UniqueConstraint(condition=models.Q(('business', None)), fields=('client',), name='unique_client'),
        ),
    ]
