
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator, EmailValidator
import datetime
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta

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

    def __str__(self):
        return f"{self.name} - {self.amount:.2f}"


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

    def __str__(self):
        return self.email  # Return the email as the string representation


class Order(models.Model):
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(verbose_name='Email Address')
    order_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    full_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    ITEM_SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large')
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
    
    def clean(self):
        # Check for suspicious patterns
        if self.ip_address:
            # Check for multiple orders from same IP
            recent_orders = Order.objects.filter(
                ip_address=self.ip_address,
                created_at__gte=timezone.now() - timedelta(hours=1)
            )
            if recent_orders.count() >= 5:
                raise ValidationError("Security check failed. Please try again later.")

        # Validate phone number format
        if not self.phone_number.startswith('+256'):
            raise ValidationError("Please enter a valid Ugandan phone number starting with +256")

    def __str__(self):
        return f"Order {self.id} by {self.full_name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"