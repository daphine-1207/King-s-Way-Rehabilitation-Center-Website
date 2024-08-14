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
            # Get cleaned data from the form
            application_data = form.cleaned_data

            # Compose the email content
            email_message = f"""
            New Application Received

            Applicant Details:
            ----------------------
            Full Name: {application_data.get('first_name')} {application_data.get('middle_name', '')} {application_data.get('last_name')}
            Address: {application_data.get('address')}
            City: {application_data.get('city')}
            Country: {application_data.get('country')}
            District: {application_data.get('district')}
            Date of Birth: {application_data.get('dob')}
            Primary Phone: {application_data.get('primary_phone')}
            Secondary Phone: {application_data.get('secondary_phone')}
            Email: {application_data.get('email')}

            Application Details:
            ----------------------
            Completing for Someone Else: {application_data.get('someone_else')}
            First Choice Treatment Centre: {application_data.get('treatment_centre')}
            18 Years or Older: {application_data.get('age')}
            Drug or Alcohol Abuse Problem: {application_data.get('abuse_problem')}
            Open to Faith-Based Treatment: {application_data.get('faith_based')}
            12-Month Commitment: {application_data.get('commitment')}
            Forced to Seek Help: {application_data.get('forced')}
            Disabilities: {application_data.get('disabilities')}
            Psychiatric Conditions: {application_data.get('psych_conditions')}
            Serious Conditions (AIDS, Cancer, TB): {application_data.get('serious_conditions')}
            Takes Medications: {application_data.get('medications')}
            Medication Details: {application_data.get('medications_details')}
            Outstanding Warrants: {application_data.get('outstanding_warrants')}
            On Parole: {application_data.get('parole')}
            In Detention Facility: {application_data.get('detention')}
            Legal Issues: {application_data.get('legal_issues')}
            Sex Offender Registry: {application_data.get('sex_offender_registry')}
            Additional Comments: {application_data.get('additional_comments')}
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