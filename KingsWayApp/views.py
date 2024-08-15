from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings


# Create your views here.
def about(request):
    return render(request, 'about.html')

def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def gallery(request):
    return render(request, 'gallery.html')

def contact(request):
    return render(request, 'contact.html')

def shop(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_data = form.cleaned_data
            message = order_data.get('message', '') 
            recipient_email = 'kingswayrehabilitation@gmail.com'  

            # Compose email content
            email_message = f"""
            New Order Received

            Order Details:
            ----------------------
            Full Name: {order_data.get('full_name')}
            Item Name: {order_data.get('item_name')}
            Item Size: {order_data.get('item_size')}
            Quantity: {order_data.get('quantity')}
            Phone Number: {order_data.get('phone_number')}
            Payment Option: {order_data.get('payment_option')}

            """
            
            # Send email
            try:
                send_mail(
                    subject='New Order Notification',
                    message=email_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient_email],
                    fail_silently=False
                )
                messages.success(request, 'Order made successfully!')
            except Exception as e:
                print(f'Error sending email: {e}')
                messages.error(request, 'There was an error sending your order.')

            # Create order
            Order.objects.create(
                full_name=order_data['full_name'],
                item_name=order_data['item_name'],
                item_size=order_data['item_size'],
                quantity=order_data['quantity'],
                phone_number=order_data['phone_number'],
                payment_option=order_data['payment_option']
            )
            return redirect('shop')
        else:
            return render(request, 'shop.html', {'form': form})
    else:
        form = OrderForm()

    return render(request, 'shop.html', {'form': form})

def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = DonationForm()
    return render(request, 'donate.html', {'form': form})


def success_view(request):
    return render(request, 'success.html')


def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application_data = form.cleaned_data

            # Compose the email content
            email_message = f"""
            New Application Received

            Applicant Details:
            ----------------------
            Surname: {application_data.get('surname')}
            Other Names: {application_data.get('other_names')}
            Marital Status: {application_data.get('marital_status')}
            Nationality: {application_data.get('nationality')}
            Date of Birth: {application_data.get('dob')}
            Place of Birth: {application_data.get('pob')}
            Age: {application_data.get('age')}
            NIN: {application_data.get('nin')}
            Passport Number: {application_data.get('passport_number')}
            Physical Address: {application_data.get('physical_address')}
            Phone Number: {application_data.get('phone_number')}

            Emergency Contact:
            ----------------------
            Full Name: {application_data.get('emergency_full_name')}
            Address: {application_data.get('emergency_address')}
            Phone Number: {application_data.get('emergency_phone_number')}
            Relationship: {application_data.get('relationship')}

            Application Details:
            ----------------------
            Completing for Someone Else: {application_data.get('someone_else')}
            Rehabilitation Setting: {application_data.get('rehabilitation_setting')}
            Rehabilitation Setting Details: {application_data.get('rehabilitation_setting_details')}
            Mental Health Treatment History: {application_data.get('mental_health_treatment')}
            Counselling Before: {application_data.get('counselling_before')}
            Main Problem: {application_data.get('main_problem')}
            Additional Comments: {application_data.get('comments')}
            """

            # Send the email
            recipient_email = 'kingswayrehabilitation@gmail.com'
            try:
                send_mail(
                    subject='New Application Notification',
                    message=email_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient_email],
                    fail_silently=False
                )
                messages.success(request, 'Application submitted successfully!')
            except Exception as e:
                print(f'Error sending email: {e}')
                messages.error(request, 'There was an error sending your application.')

            return redirect('success')
        else:
            messages.error(request, 'Please correct the errors in the form.')

    else:
        form = ApplicationForm()

    return render(request, 'application_form.html', {'form': form})

