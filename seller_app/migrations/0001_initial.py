# Generated by Django 4.1.13 on 2024-11-06 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product_app", "0001_initial"),
        ("customer_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Seller",
            fields=[
                ("seller_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("shop_address", models.CharField(max_length=255)),
                ("phone_number", models.CharField(max_length=15, unique=True)),
                ("username", models.CharField(max_length=50, unique=True)),
                ("password", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("order_id", models.AutoField(primary_key=True, serialize=False)),
                ("quantity", models.IntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("delivered", "Delivered"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("total_bill", models.FloatField()),
                (
                    "customer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customer_app.customer",
                    ),
                ),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product_app.product",
                    ),
                ),
                (
                    "seller_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="seller_app.seller",
                    ),
                ),
            ],
        ),
    ]
