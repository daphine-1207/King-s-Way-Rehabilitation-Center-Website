from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from .forms import *
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.utils import timezone



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



@require_http_methods(["GET", "POST"])
def shop(request):
    if request.method == 'POST':
        # Rate limiting check
        ip = request.META.get('REMOTE_ADDR')
        current_hour = timezone.now().hour
        cache_key = f'order_count_{ip}_{current_hour}'
        
        if cache.get(cache_key, 0) >= 5:
            messages.error(request, 'Too many orders. Please try again in an hour.')
            return HttpResponseForbidden('Too many orders. Please try again later.')

        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                # Create order instance but don't save yet
                order = form.save(commit=False)
                
                # Add security tracking fields
                order.ip_address = request.META.get('REMOTE_ADDR')
                order.user_agent = request.META.get('HTTP_USER_AGENT', '')
                order.created_at = timezone.now()
                
                # Get cleaned form data
                order_data = form.cleaned_data

                # Compose email content
                email_message = f"""
                New Order Received

                Order Details:
                ----------------------
                Full Name: {order_data.get('full_name')}
                Email: {order_data.get('email')}
                Item Name: {order_data.get('item_name')}
                Item Size: {order_data.get('item_size')}
                Quantity: {order_data.get('quantity')}
                Delivery Address: {order_data.get('delivery_address')}
                Phone Number: {order_data.get('phone_number')}
                Payment Option: {order_data.get('payment_option')}

                Security Information:
                ----------------------
                IP Address: {order.ip_address}
                Order Time: {order.created_at}
                """

                # Send email notification
                send_mail(
                    subject='New Order Notification',
                    message=email_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['kingswayrehabilitation@gmail.com'],
                    fail_silently=False
                )

                # Save the order
                order.save()

                # Increment rate limit counter
                cache.set(cache_key, cache.get(cache_key, 0) + 1, 3600)  # Expires in 1 hour

                messages.success(request, 'Order placed successfully! We will contact you soon.')
                return redirect('shop')

            except Exception as e:
                # Log the error (you should set up proper logging)
                print(f'Error processing order: {e}')
                messages.error(request, 'There was an error processing your order. Please try again.')
                return render(request, 'shop.html', {'form': form})

        else:
            # Form validation failed
            messages.error(request, 'Please correct the errors in your form.')
            return render(request, 'shop.html', {'form': form})

    else:
        # GET request - display empty form
        form = OrderForm()

    # Add CSRF token to context
    context = {
        'form': form,
        'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY,  # If using recaptcha
    }

    return render(request, 'shop.html', context)

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


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_data = form.cleaned_data
            recipient_email =  'kingswayrehabilitation@gmail.com'  

            # Compose email content
            email_message = f"""
            New Contact Form Submission

            Details:
            ----------------------
            Name: {contact_data.get('name')}
            Email: {contact_data.get('email')}
            Message: {contact_data.get('message')}
            """

            # Send email
            try:
                send_mail(
                    subject='New Contact Form Submission',
                    message=email_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient_email],
                    fail_silently=False
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                print(f'Error sending email: {e}')
                messages.error(request, 'There was an error sending your message.')

            return redirect('success')  
        else:
            return render(request, 'contact.html', {'form': form})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save()

            # Send an email to the site administrators
            admin_subject = 'New Newsletter Subscription'
            admin_message = f'A new subscriber has signed up with the email: {subscriber.email}'
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,  
                ['kingswayrehabilitation@gmail.com'],  
                fail_silently=False,
            )

            # Send a thank you email to the subscriber
            subscriber_subject = 'Thank You for Subscribing to Our Newsletter'
            subscriber_message = f'Dear {subscriber.name},\n\nThank you for subscribing to our newsletter. Stay tuned for updates!'
            send_mail(
                subscriber_subject,
                subscriber_message,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],  
                fail_silently=False,
            )

            return redirect('index')
    else:
        form = SubscriptionForm()

    return render(request, 'base.html', {'form': form})

