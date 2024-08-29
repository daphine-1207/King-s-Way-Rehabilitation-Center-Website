from django import forms
from .models import *

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
        validators=[MinValueValidator(1)], 
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
 
    class Meta:
        model = Order
        fields = ['full_name', 'item_name', 'item_size', 'quantity', 'phone_number', 'delivery_address', 'payment_option']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'item_name': forms.Select(choices=Order.ITEM_CHOICES,attrs={'class': 'form-control', 'id': 'item_size_select'}),
            'item_size': forms.Select(choices=Order.ITEM_SIZE_CHOICES,attrs={'class': 'form-control', 'id': 'item_size_select'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your delivery address'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your payment method'}),

}

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(label="Email address")
    message = forms.CharField(widget=forms.Textarea, label="Message")
