
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator, EmailValidator
import datetime
from django.utils.translation import gettext_lazy as _

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
    name = models.CharField(max_length=100, blank=True, validators=[validate_name])
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.email


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



def validate_dob(value):
    if value > datetime.date.today():
        raise ValidationError(
            _('Date of birth cannot be in the future.'),
            params={'value': value},
        )

def nin_validator(value):
    pattern = r'^[A-Z0-9]{6,20}$' 
    if not re.match(pattern, value):
        raise ValidationError(
            'NIN must be between 6 and 20 alphanumeric characters long.'
)

passport_number_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9]{6,14}$',
    message="Passport number must be between 6 and 14 alphanumeric characters."
)

phone_number_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Enter a valid phone number."
)

class Application(models.Model):
    # Personal Information
    surname_name = models.CharField(max_length=100, validators=[validate_name, MinLengthValidator(2)])
    other_names = models.CharField(max_length=200, validators=[validate_name, MinLengthValidator(2)])
    marital_status = models.BooleanField()
    nationality = models.CharField(max_length=100, blank=False, null=False, validators=[validate_name, MinLengthValidator(4)])
    dob = models.DateField(validators=[validate_dob])
    pob = models.CharField(max_length=100, blank=False, null=False, validators=[MaxLengthValidator(100)])
    age = models.IntegerField()
    nin = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=10, validators=[passport_number_validator], blank=True, null=True)
    physical_address = models.CharField(max_length=100, validators=[validate_name, MinLengthValidator(4)])
    phone_number = models.CharField(max_length=17, validators=[phone_number_validator])

    #Incase of Emergecncy
    full_name = models.CharField (max_length=200, validators=[validate_name, MinLengthValidator(5)])
    address = models.CharField(max_length=100, validators=[validate_name, MinLengthValidator(4)])
    emergency_phone_number = models.CharField(max_length=17, validators=[phone_number_validator])
    relationship = models.CharField(max_length=100)
    
    # Application Details
    someone_else = models.BooleanField()
    rehabilitation_setting = models.BooleanField()
    rehabilitation_setting_details = models.TextField(blank=True, null=True)
    mental_health_treatment = models.BooleanField()
    counselling_before = models.BooleanField()
    main_problem = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    
    def _str_(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"
    

# class Contact(models.Model):
#     name = models.CharField(max_length=100, blank=True, validators=[validate_name])
#     email = models.EmailField(unique=True)
#     message = models.TextField(max_length=500)

#     def _str_(self):
#         return self.name