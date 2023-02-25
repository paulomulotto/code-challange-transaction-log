# Generated by Django 3.2.18 on 2023-02-25 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('number', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='client.client')),
            ],
        ),
    ]
