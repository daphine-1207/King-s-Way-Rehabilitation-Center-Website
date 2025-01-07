from django.test import TestCase
from .models import *
import re
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone


class DonationModelTest(TestCase):

    def setUp(self):
        # Set up a valid donation instance for testing
        self.donation = Donation.objects.create(
            amount=100.00,
            name="John Doe",
            email="john.doe@example.com",
            payment_method="credit_card"
        )

    def test_donation_creation(self):
        # Test if the donation was created correctly
        self.assertEqual(self.donation.amount, 100.00)
        self.assertEqual(self.donation.name, "John Doe")
        self.assertEqual(self.donation.email, "john.doe@example.com")
        self.assertEqual(self.donation.payment_method, "credit_card")
        self.assertIsNotNone(self.donation.created_at)

    def test_str_method(self):
        # Test the __str__ method of the Donation model
        self.assertEqual(str(self.donation), "John Doe - 100.00")

    def test_invalid_payment_method(self):
    # Test if invalid payment method raises a ValidationError
      with self.assertRaises(ValidationError):
        invalid_donation = Donation(
            amount=50.00,
            name="Jane Doe",
            email="jane.doe@example.com",
            payment_method="cash"  # Invalid payment method
        )
        invalid_donation.full_clean()  # Triggers model validation


    def test_valid_name(self):
        # Test that the name is valid if it contains letters and spaces
        try:
            validate_name("John Doe")  # Valid name
        except ValidationError:
            self.fail("validate_name raised ValidationError unexpectedly!")

    def test_invalid_name_length(self):
        # Test that the name validation raises an error for names shorter than 2 characters
        with self.assertRaises(ValidationError):
            validate_name("J")  # Name is too short

    def test_invalid_name_characters(self):
        # Test that the name validation raises an error for names containing non-alphabetical characters
        with self.assertRaises(ValidationError):
            validate_name("John123")  # Invalid characters

class SubscriptionModelTest(TestCase):

    def test_create_subscription(self):
        # Create a valid subscription
        subscription = Subscription.objects.create(
            name="John Doe",
            email="john.doe@example.com"
        )
        self.assertEqual(subscription.name, "John Doe")
        self.assertEqual(subscription.email, "john.doe@example.com")
        self.assertIsNotNone(subscription.subscribed_at)  # Ensure the date was automatically added

    def test_duplicate_email(self):
        # Create the first subscription
        Subscription.objects.create(
            name="Jane Doe",
            email="jane.doe@example.com"
        )
        # Try creating another subscription with the same email
        with self.assertRaises(ValidationError):
            subscription = Subscription(
                name="John Smith",
                email="jane.doe@example.com"
            )
            subscription.full_clean()  # This triggers validation

    def test_str_method(self):
        # Create a subscription and check the __str__ method
        subscription = Subscription.objects.create(
            name="John Doe",
            email="john.doe@example.com"
        )
        self.assertEqual(str(subscription), "john.doe@example.com")


class SubscriberModelTest(TestCase):

    def test_create_subscriber(self):
        # Create a valid subscriber
        subscriber = Subscriber.objects.create(
            name="John Doe",
            email="john.doe@example.com"
        )
        self.assertEqual(subscriber.name, "John Doe")
        self.assertEqual(subscriber.email, "john.doe@example.com")

    def test_duplicate_email(self):
        # Create the first subscriber
        Subscriber.objects.create(
            name="Jane Doe",
            email="jane.doe@example.com"
        )
        # Try creating another subscriber with the same email
        with self.assertRaises(ValidationError):
            subscriber = Subscriber(
                name="John Smith",
                email="jane.doe@example.com"
            )
            subscriber.full_clean()  # This triggers validation

    def test_str_method(self):
        # Create a subscriber and check the __str__ method
        subscriber = Subscriber.objects.create(
            name="John Doe",
            email="john.doe@example.com"
        )
        self.assertEqual(str(subscriber), "john.doe@example.com")

class OrderModelTest(TestCase):

    def test_create_valid_order(self):
        # Create a valid order
        order = Order.objects.create(
            ip_address="192.168.0.1",
            user_agent="Mozilla/5.0",
            email="customer@example.com",
            order_status="pending",
            full_name="John Doe",
            item_name="Mens_TShirt",
            item_size="M",
            quantity=1,
            phone_number="+256700633321",
            delivery_address="123 Test Street",
            payment_option="Cash-On-Delivery"
        )
        self.assertEqual(order.full_name, "John Doe")
        self.assertEqual(order.phone_number, "+256700633321")
        self.assertEqual(order.payment_option, "Cash-On-Delivery")

    def test_invalid_phone_number(self):
        # Create an order with an invalid phone number
        order = Order(
            ip_address="192.168.0.1",
            user_agent="Mozilla/5.0",
            email="customer@example.com",
            order_status="pending",
            full_name="John Doe",
            item_name="Mens_TShirt",
            item_size="M",
            quantity=1,
            phone_number="+123456789",
            delivery_address="123 Test Street",
            payment_option="Cash-On-Delivery"
        )
        with self.assertRaises(ValidationError):
            order.full_clean()  # This will trigger the validation error for phone number

    def test_security_check_on_ip_address(self):
        # Create multiple orders with the same IP within an hour
        ip_address = "192.168.0.1"
        for _ in range(5):
            Order.objects.create(
                ip_address=ip_address,
                user_agent="Mozilla/5.0",
                email="customer@example.com",
                order_status="pending",
                full_name="John Doe",
                item_name="Mens_TShirt",
                item_size="M",
                quantity=1,
                phone_number="+256700633321",
                delivery_address="123 Test Street",
                payment_option="Cash-On-Delivery"
            )
        
        # Now try creating a 6th order from the same IP (it should raise a ValidationError)
        order = Order(
            ip_address=ip_address,
            user_agent="Mozilla/5.0",
            email="customer2@example.com",
            order_status="pending",
            full_name="Jane Doe",
            item_name="Baby_Sweater",
            item_size="L",
            quantity=1,
            phone_number="+256700633322",
            delivery_address="124 Test Street",
            payment_option="Mobile_Money"
        )
        with self.assertRaises(ValidationError):
            order.full_clean()  # This will trigger the security check validation

    def test_str_method(self):
        # Create an order and check the __str__ method
        order = Order.objects.create(
            ip_address="192.168.0.1",
            user_agent="Mozilla/5.0",
            email="customer@example.com",
            order_status="pending",
            full_name="John Doe",
            item_name="Mens_TShirt",
            item_size="M",
            quantity=1,
            phone_number="+256700633321",
            delivery_address="123 Test Street",
            payment_option="Cash-On-Delivery"
        )
        self.assertEqual(str(order), f"Order {order.id} by John Doe")

class ContactModelTest(TestCase):

    def test_contact_str_method(self):
        # Create a Contact instance
        contact = Contact.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            message="This is a test message."
        )
        
        # Check if the string representation of the contact is as expected
        self.assertEqual(str(contact), "John Doe - john.doe@example.com")

    def test_contact_model_creation(self):
        # Create a Contact instance
        contact = Contact.objects.create(
            name="Jane Smith",
            email="jane.smith@example.com",
            message="Hello, I have a question."
        )
        
        # Check if the contact was created and saved correctly
        self.assertEqual(contact.name, "Jane Smith")
        self.assertEqual(contact.email, "jane.smith@example.com")
        self.assertEqual(contact.message, "Hello, I have a question.")
        self.assertIsInstance(contact, Contact)