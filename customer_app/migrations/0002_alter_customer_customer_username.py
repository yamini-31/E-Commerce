# Generated by Django 4.2.16 on 2024-11-06 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_username',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
