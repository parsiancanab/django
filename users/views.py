from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SubscribeForm, SubscriptionForm
from blog.models import Subscriber, Subscription
from django.core.mail import send_mail
from datetime import datetime
from calendar import HTMLCalendar
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model


User = get_user_model()


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your subscription has been confirmed!")
        return redirect("blog-blog")
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect("blog-blog")
    

def send_approved_email(request, firstname):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Create user but set is_active=False until email is confirmed
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # User cannot login until email is confirmed
        user.save()

        # Send confirmation email
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirmation_link = f"http://{request.get_host()}/activate/{uid}/{token}/"

        subject = 'Subscription Approved'
        message = render_to_string('users/confirmation_email.html', {
            'user': user,
            'confirmation_link': confirmation_link,
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        messages.success(request, 'A confirmation email has been sent to your email address.')
        return redirect('login')
    
    return render(request, 'users/approved_registration.html')
# f'Dear {firstname},\n\nYour subscription has been successfully approved. Thank you for subscribing!'

# users/views.py
def subscription_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # User cannot login until email is confirmed
        user.save()

        # Send confirmation email to user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirmation_link = f"http://{request.get_host()}/activate/{uid}/{token}/"
        subject = 'Confirm Your Registration'
        message = render_to_string('users/confirmation_email.html', {
            'user': user,
            'confirmation_link': confirmation_link,
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        # Send approval email to admin
        admin_subject = 'New User Registration Approval'
        admin_message = f'A new user {username} ({email}) has registered and is awaiting approval.'
        send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, ['yavari.milad@yahoo.com'])

        messages.success(request, 'A confirmation email has been sent to your email address.')
        return redirect('login')
    
    return render(request, 'users/subscription.html')

# Utility function to send activation email
def send_activation_email(email, firstname):
    subject = 'Subscription Activation'
    message = f'Dear {firstname},\n\nYour subscription has been successfully activated. Thank you for subscribing!'
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        return True
    except Exception as e:
        return False

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login and mention posts.')
            return redirect('login')
        
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# User profile view
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'u_form': u_form, 'p_form': p_form})

# Subscription view
# Subscriber list view
def subscriber_list(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'users/subscriber_list.html', {'subscribers': subscribers})


def subscription_list(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'users/subscription_list.html', {'subscribers': subscriptions})


# users/views.py
def registered(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if username/email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('registered')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('registered')

        # Proceed with user creation
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # Rest of your email sending logic...
    
    return render(request, 'users/registered.html')


def generate_activation_token(email):
    """Generate a secure activation token using user's email"""
    return default_token_generator.make_token(Subscriber(email=email))


def send_activation_email(subscriber, request):
    """Send activation email with tokenized link"""
    token = generate_activation_token(subscriber.email)
    uid = urlsafe_base64_encode(force_bytes(subscriber.pk))
    
    activation_link = f"{request.scheme}://{request.get_host()}/activate/{uid}/{token}/"
    
    subject = "Activate Your Subscription"
    message = render_to_string('users/activation_email.html', {
        'subscriber': subscriber,
        'activation_link': activation_link,
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [subscriber.email],
        fail_silently=False
    )

# Date and time view
def show_datetime(request):
    current_time = datetime.now().time()
    current_date = datetime.now().date()
    calendar_html = HTMLCalendar().formatmonth(datetime.now().year, datetime.now().month)
    return render(request, 'users/datetime.html', {
        'current_time': current_time,
        'calendar_html': calendar_html,
        'current_date': current_date
    })