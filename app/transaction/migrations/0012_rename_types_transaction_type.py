# Generated by Django 3.2.18 on 2023-02-27 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0011_auto_20230227_0055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='types',
            new_name='type',
        ),
    ]
