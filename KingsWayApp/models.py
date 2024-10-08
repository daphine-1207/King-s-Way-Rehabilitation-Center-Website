
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator, EmailValidator
import datetime
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

class Donation(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.name} - {self.amount}"


def validate_name(value):
    if len(value) < 2:
        raise ValidationError('Name must be at least 2 characters long.')
    if not re.match("^[a-zA-Z ]*$", value):
        raise ValidationError(
            '%(value)s is not a valid name. Only letters and spaces are allowed.',
            params={'value': value},
        )


class Subscription(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Order(models.Model):
    full_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    ITEM_SIZE_CHOICES = [
        ('Extra Small', 'Extra Small'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('Extra Large', 'Extra Large'),
    ]
    ITEM_CHOICES = [
        ('Mens_TShirt', "Men's T-Shirt"),
        ('Baby_Sweater', 'Baby Sweater'),
        ('Womens_TShirt', "Women's T-Shirt"),
        ('Jumper', 'Jumper'),
        ('Bottle', 'Bottle'),
        ('Wristband', 'Wristband'),
        ('Cap', 'Cap'),
        ('Umbrella', 'Umbrella'),
        ('Notebook', 'Notebook'),
]
    item_name = models.CharField(max_length=255, choices=ITEM_CHOICES, blank=False, null=False)
    item_size = models.CharField(max_length=20, choices=ITEM_SIZE_CHOICES, blank=True, null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    phone_number = models.CharField(
        max_length=16, 
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',  
                message="Phone number must be entered in the format: '+123456789'. Up to 15 digits allowed."
            ),
        ],
        help_text="Enter your phone number with country code, e.g., +256700633321"
    )
    delivery_address = models.CharField(max_length=100)
    PAYMENT_OPTIONS = [
        ('Cash-On-Delivery', 'Cash on Delivery'),
        ('Mobile_Money', 'Mobile Money'),
    ]
    payment_option = models.CharField(max_length=30, choices=PAYMENT_OPTIONS)
    

    def _str_(self):
        return f"Order {self.id} by {self.full_name}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"