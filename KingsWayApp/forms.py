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

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'surname_name', 'other_names', 'marital_status', 'nationality', 'dob', 'pob', 
            'age', 'nin', 'passport_number', 'physical_address', 'phone_number', 
            'full_name', 'emergency_phone_number', 'relationship', 'someone_else', 
            'rehabilitation_setting', 'rehabilitation_setting_details', 'mental_health_treatment', 
            'counselling_before', 'main_problem', 'comments'
        ]


    def clean(self):
        cleaned_data = super().clean()
        boolean_fields = ['marital_status', 'someone_else', 'rehabilitation_setting', 'mental_health_treatment', 'counselling_before']

        for field in boolean_fields:
            value = cleaned_data.get(field)
            if value in ['Yes', 'No']:
                cleaned_data[field] = True if value == 'Yes' else False

        return cleaned_data


    # Personal Information
    surname_name = forms.CharField(
        label="Surname", max_length=100, validators=[validate_name, MinLengthValidator(2)], required=True
    )
    other_names = forms.CharField(
        label="Other Names", max_length=200, validators=[validate_name, MinLengthValidator(2)], required=True
    )
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('Yes', 'Yes'), ('No', 'No')],
        required=True
    )
    nationality = forms.CharField(
        label="Nationality", max_length=100, validators=[MinLengthValidator(4)], required=True
    )
    dob = forms.DateField(
        label="Date of Birth", required=True, widget=forms.TextInput(attrs={'type': 'date'})
    )
    pob = forms.CharField(
        label="Place of Birth", max_length=100, validators=[MaxLengthValidator(100)], required=True
    )
    age = forms.IntegerField(label="Age", required=True, widget=forms.TextInput(attrs={
            'style': 'width: 100%;'})
    )
    nin = forms.CharField(
        label="National Identification Number (NIN)", required=False
    )
    passport_number = forms.CharField(
        label="Passport Number", validators=[passport_number_validator], required=False
    )
    physical_address = forms.CharField(
        label="Physical Address",validators=[MinLengthValidator(4)], required=True
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=17, validators=[phone_number_validator], required=True, widget=forms.TextInput(attrs={
            'placeholder': 'Enter number with your country code'})
    )

    # Emergency Contact
    full_name = forms.CharField(
        label="Full Name", max_length=200, validators=[validate_name, MinLengthValidator(5)], required=True
    )
    emergency_phone_number = forms.CharField(
        label="Phone Number", max_length=17, validators=[phone_number_validator], required=True, widget=forms.TextInput(attrs={
            'placeholder': 'Enter number with your country code'})
    )
    address = forms.CharField(
        label="Address",validators=[MinLengthValidator(4)], required=True
    )
    relationship = forms.CharField(
        label="Relationship", max_length=100, required=True
    )

    # Application Details
    someone_else = forms.ChoiceField(
        label="Are you completing this application for someone else?", 
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.RadioSelect, required=True
    )
    rehabilitation_setting = forms.ChoiceField(
        label="Have you been in a rehabilitation setting before?", 
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.RadioSelect, required=True
    )
    rehabilitation_setting_details = forms.CharField(
        label="If yes, details of Rehabilitation Setting", widget=forms.Textarea(attrs={'rows': 4}), required=False
    )
    mental_health_treatment = forms.ChoiceField(
        label="Have you ever received mental health treatment?", 
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.RadioSelect, required=True
    )
    counselling_before = forms.ChoiceField(
        label="Have you had counselling before?", 
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.RadioSelect, required=True
    )
    main_problem = forms.CharField(
        label="Main Problem", widget=forms.Textarea(attrs={'rows': 4}), required=False
    )
    comments = forms.CharField(
        label="Additional Comments", widget=forms.Textarea(attrs={'rows': 5}), required=False
    )


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['name', 'email', 'message']