from django import forms
from .models import *

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'name', 'email', 'payment_method']
from .models import Subscription

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

    ITEM_SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('extra_large', 'Extra Large'),  
    ]
    
    item_size = forms.ChoiceField(
        choices=ITEM_SIZE_CHOICES,
        widget=forms.RadioSelect,
        label='Jumper/Shirt Size'
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
            'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your delivery address'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your payment method'}),

        }

class ApplicationForm(forms.Form):
    # Contact Information
    first_name = forms.CharField(label="First Name", max_length=100, required=True)
    middle_name = forms.CharField(label="Middle Name", max_length=100, required=False)
    last_name = forms.CharField(label="Last Name", max_length=100, required=True)
    address = forms.CharField(label="Address", max_length=255, required=True)
    city = forms.CharField(label="City", max_length=100, required=True)
    country = forms.CharField(label="Country", max_length=100, required=True)
    district = forms.CharField(label="District", max_length=100, required=True)
    dob = forms.DateField(label="Date of Birth", required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    email = forms.EmailField(label="Email Address", required=True)
    primary_phone = forms.CharField(label="Primary Phone Number", max_length=15, required=True)
    secondary_phone = forms.CharField(label="Secondary Phone Number", max_length=15, required=False)

    # Application Details
    someone_else = forms.ChoiceField(
        label="Are you completing this application for someone else?", 
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    treatment_centre = forms.CharField(label="What is your first choice for a treatment centre?", max_length=255, required=False)
    age = forms.ChoiceField(
        label="Are you 18 years of age or older?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    abuse_problem = forms.ChoiceField(
        label="Do you have a drug or alcohol abuse problem or addiction?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    faith_based = forms.ChoiceField(
        label="Are you open to a Christian faith-based approach to treatment?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    commitment = forms.ChoiceField(
        label="Are you open to a 12-month commitment to treatment?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    forced = forms.ChoiceField(
        label="Is someone else forcing you to seek help?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    disabilities = forms.ChoiceField(
        label="Do you have disabilities that would prevent full participation in regular physical activities?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    psych_conditions = forms.ChoiceField(
        label="Do you have any other psychiatric conditions?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    serious_conditions = forms.ChoiceField(
        label="Do you have full-blown AIDS, cancer, or tuberculosis?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    medications = forms.ChoiceField(
        label="Do you take medications? If so, what?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    medications_details = forms.CharField(label="Medication Details", widget=forms.Textarea(attrs={'rows': 4}), required=False)
    outstanding_warrants = forms.ChoiceField(
        label="Do you have outstanding warrants?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    parole = forms.ChoiceField(
        label="Are you on parole?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    detention = forms.ChoiceField(
        label="Are you currently in jail, prison, or other detention facility?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    legal_issues = forms.ChoiceField(
        label="Do you have outstanding court or legal issues? If so, what?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    sex_offender_registry = forms.ChoiceField(
        label="Are you listed on the national sex offender registry?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, required=True
    )
    additional_comments = forms.CharField(
        label="Anything else we need to know? Medication? Legal? Health concerns?",
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False
    )
