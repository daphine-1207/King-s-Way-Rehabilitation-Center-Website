# Generated by Django 5.0.7 on 2024-08-29 14:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Donation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("credit_card", "Credit Card"),
                            ("paypal", "PayPal"),
                            ("bank_transfer", "Bank Transfer"),
                        ],
                        max_length=50,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=100)),
                (
                    "item_name",
                    models.CharField(
                        choices=[
                            ("Mens_TShirt", "Men's T-Shirt"),
                            ("Baby_Sweater", "Baby Sweater"),
                            ("Womens_TShirt", "Women's T-Shirt"),
                            ("Jumper", "Jumper"),
                            ("Bottle", "Bottle"),
                            ("Wristband", "Wristband"),
                            ("Cap", "Cap"),
                            ("Umbrella", "Umbrella"),
                            ("Notebook", "Notebook"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "item_size",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Extra Small", "Extra Small"),
                            ("Small", "Small"),
                            ("Medium", "Medium"),
                            ("Large", "Large"),
                            ("Extra Large", "Extra Large"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        help_text="Enter your phone number with country code, e.g., +256700633321",
                        max_length=16,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+123456789'. Up to 15 digits allowed.",
                                regex="^\\+?\\d{7,15}$",
                            )
                        ],
                    ),
                ),
                ("delivery_address", models.CharField(max_length=100)),
                (
                    "payment_option",
                    models.CharField(
                        choices=[
                            ("Cash-On-Delivery", "Cash on Delivery"),
                            ("Mobile_Money", "Mobile Money"),
                        ],
                        max_length=30,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("subscribed_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
