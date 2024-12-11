from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Donation, Order

# Tests for the Donation model
class DonationModelTest(TestCase):
    def test_amount_is_positive(self):
        # Creating a Donation instance with a negative amount
        donation = Donation(amount=-10.00, name='John Doe', email='john@example.com', payment_method='credit_card')
        
        # Check for ValidationError when calling full_clean
        with self.assertRaises(ValidationError):
            donation.full_clean()

    def test_valid_email(self):
        # Creating a Donation instance with an invalid email
        donation = Donation(amount=50.00, name='John Doe', email='invalid-email', payment_method='credit_card')
        
        # Check for ValidationError when calling full_clean
        with self.assertRaises(ValidationError):
            donation.full_clean()

    def test_valid_payment_method(self):
        # Creating a Donation instance with an invalid payment method
        donation = Donation(amount=50.00, name='John Doe', email='john@example.com', payment_method='invalid_method')
        
        # Check for ValidationError when calling full_clean
        with self.assertRaises(ValidationError):
            donation.full_clean()

# Tests for the Order model
class OrderModelTest(TestCase):
    def test_quantity_is_positive(self):
        # Creating an Order instance with a quantity less than 1
        order = Order(full_name='Jane Doe', item_name='Mens_TShirt', quantity=0, phone_number='+123456789', delivery_address='123 Main St', payment_option='Cash-On-Delivery')
        
        # Check for ValidationError when calling full_clean
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_valid_phone_number_format(self):
        # Creating an Order instance with an invalid phone number
        order = Order(full_name='Jane Doe', item_name='Mens_TShirt', quantity=1, phone_number='12345', delivery_address='123 Main St', payment_option='Cash-On-Delivery')
        
        # Check for ValidationError when calling full_clean
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_payment_option_choices(self):
        # Creating an Order instance with an invalid payment option
        order = Order(full_name='Jane Doe', item_name='Mens_TShirt', quantity=1, phone_number='+123456789', delivery_address='123 Main St', payment_option='InvalidOption')
        
        # Check for ValidationError when calling full_clean
        with self.assertRaises(ValidationError):
            order.full_clean()
