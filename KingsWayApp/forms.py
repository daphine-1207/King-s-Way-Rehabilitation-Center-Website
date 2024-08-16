from django import forms
from .models import *

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'name', 'email', 'payment_method']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']  
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
        }
    email = forms.EmailField(required=True)


class OrderForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message="Phone number must be entered in the format: '+123456789'. Up to 15 digits allowed."
            ),
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number with country code'
        }),
    )

    quantity = forms.IntegerField(
        validators=[MinValueValidator(1)],  # Ensure quantity is positive
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter quantity'
        })
    )
    PAYMENT_CHOICES = [
            ('Mobile_Money', 'Mobile Money'),
            ('Cash-On-Delivery', 'Cash on Delivery'),
        ]
        
    payment_option = forms.ChoiceField(
            choices=PAYMENT_CHOICES,
            widget=forms.RadioSelect,  
            label='Payment Option'
        )

 
    class Meta:
        model = Order
        fields = ['full_name', 'item_name', 'item_size', 'quantity', 'phone_number', 'delivery_address', 'payment_option']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your item name'}),
            'item_size': forms.Select(choices=Order.ITEM_SIZE_CHOICES,attrs={'class': 'form-control', 'id': 'item_size_select'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your delivery address'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your payment method'}),

        }
