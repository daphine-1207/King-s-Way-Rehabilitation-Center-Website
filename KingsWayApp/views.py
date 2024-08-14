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
            recipient_email = 'kingswayrehabilitation@gmail.com'  # Fixed recipient

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

def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Thank you for your application. We will review it and contact you soon.')
            return redirect('success')  
    else:
        form = ApplicationForm()
    
    return render(request, 'application_form.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')


# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             # Process the data in form.cleaned_data
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']

#             # Send an email
#             subject = f"New Team Member Application: {name}"
#             message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
#             send_mail(
#                 subject,
#                 message_body,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [settings.DEFAULT_FROM_EMAIL],  
#             )

#             return redirect('contact') 
#     else:
#         form = ContactForm()
#     return render(request, 'contact.html', {'form': form})