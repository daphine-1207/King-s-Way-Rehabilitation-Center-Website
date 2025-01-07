from django import forms
from .models import *
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.core.validators import MinValueValidator, MaxValueValidator



class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'name', 'email', 'payment_method']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email


class OrderForm(forms.ModelForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),  # Note the parentheses to instantiate the widget
        label=''
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    confirm_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your email address'
        })
    )
    phone_number = forms.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\+256\d{9}$',  # Specific to Uganda phone numbers
                message="Phone number must be a valid Ugandan number starting with '+256' followed by 9 digits."
            ),
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Ugandan phone number (+256...)'
        }),
    )

    quantity = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter quantity (max 10)'
        })
    )

    PAYMENT_CHOICES = [
        ('Mobile_Money', 'Mobile Money'),
        ('Cash-On-Delivery', 'Cash on Delivery'),
    ]
    
    payment_option = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'}),
        label='Payment Option'
    )

    class Meta:
        model = Order
        fields = [
            'full_name', 
            'email', 
            'confirm_email', 
            'item_name', 
            'item_size', 
            'quantity', 
            'phone_number', 
            'delivery_address', 
            'payment_option'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your full name'
            }),
            'item_name': forms.Select(
                choices=[
            ('Mens_TShirt', "Men's T-Shirt"),
            ('Baby_Sweater', 'Baby Sweater'),
            ('Womens_TShirt', "Women's T-Shirt"),
            ('Jumper', 'Jumper'),
            ('Bottle', 'Bottle'),
            ('Wristband', 'Wristband'),
            ('Cap', 'Cap'),
            ('Umbrella', 'Umbrella'),
            ('Notebook', 'Notebook'),
    ],  
                attrs={
                    'class': 'form-control', 
                    'id': 'item_name_select'  # Changed from item_size_select
                }
            ),
            'item_size': forms.Select(
                choices=[
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large')
        ],
        attrs={
            'class': 'form-control', 
            'id': 'item_size_select'
        }
            ),
            'delivery_address': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your delivery address'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Check if 'item_name' is present in POST data or initial data
        item_name = self.initial.get('item_name') or self.data.get('item_name')
        if item_name:
            self.fields['item_size'].widget.choices = self.get_size_choices(item_name)
    
    def get_size_choices(self, item_name):
        """Return size choices based on selected item"""
        COMMON_SIZES = [('', 'Select Size')]
        CLOTHING_SIZES = COMMON_SIZES + [
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large')
        ]
        NON_SIZED_ITEMS = COMMON_SIZES + [('ONE_SIZE', 'One Size')]
        
        # Check the item name and return appropriate choices
        if item_name in ['Mens_TShirt', 'Womens_TShirt', 'Baby_Sweater', 'Jumper']:
            return CLOTHING_SIZES
        elif item_name in ['Bottle', 'Wristband', 'Cap', 'Umbrella', 'Notebook']:
            return NON_SIZED_ITEMS
        return COMMON_SIZES



    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')

        if email and confirm_email and email != confirm_email:
            raise ValidationError("Email addresses must match.")

        return cleaned_data

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity > 10:
            raise ValidationError("Maximum order quantity is 10 items.")
        return quantity

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.startswith('+256'):
            raise ValidationError("Please enter a valid Ugandan phone number starting with +256")
        return phone

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(label="Email address")
    message = forms.CharField(widget=forms.Textarea, label="Message")
