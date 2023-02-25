# Generated by Django 3.2.18 on 2023-02-25 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_business'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='company',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.business'),
        ),
        migrations.AlterField(
            model_name='business',
            name='code',
            field=models.CharField(default=None, max_length=15, unique=True),
        ),
    ]
