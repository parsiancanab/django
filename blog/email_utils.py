from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.contrib import messages
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.http import Http404
from django.urls import reverse
import logging
from urllib.parse import quote
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.http import Http404

# Set up logging
logger = logging.getLogger(__name__)

def activate(request, uidb64, token):
    next_url = request.GET.get("next", "blog-home")  # Default to "blog-home"
    try:
        # Decode the user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Token is valid, activate the user
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        return redirect(next_url)  # Redirect to the specified next_url

    messages.error(request, "The activation link is invalid or expired.")
    raise Http404("Invalid activation link")

def send_activation_email(request, subscriber, next_url="blog-home"):
    if not subscriber or not subscriber.email:
        logger.warning("Subscriber email is missing.")
        return

    user = User.objects.filter(email=subscriber.email).first()
    if not user:
        logger.warning(f"No user found with email: {subscriber.email}")
        return

    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    # Encode `next_url` to handle special characters
    encoded_next_url = quote(next_url, safe="")

    activation_url = reverse("activate", kwargs={"uidb64": uidb64, "token": token})
    activation_link = request.build_absolute_uri(f"{activation_url}?next={encoded_next_url}")

    html_message = render_to_string(
        "blog/activation_email.html",
        {"user": user, "activation_link": activation_link}
    )
    plain_message = strip_tags(html_message)

    subject = "Activate Your Subscription"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [subscriber.email]

    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=html_message
        )
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")  # Use logging instead of print



def send_activation_email(request, subscriber, next_url="blog-home"):  # Default to "blog-home"
    if not subscriber or not subscriber.email:
        print("Subscriber email is missing.")
        return

    user = User.objects.filter(email=subscriber.email).first()
    if not user:
        print(f"No user found with email: {subscriber.email}")
        return

    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    # Use dynamic `next_url` instead of hardcoded "blog-blog"
    activation_url = reverse("activate", kwargs={"uidb64": uidb64, "token": token})
    activation_link = request.build_absolute_uri(f"{activation_url}?next={next_url}")

    html_message = render_to_string(
        "blog/activation_email.html",
        {"user": user, "activation_link": activation_link}
    )
    plain_message = strip_tags(html_message)

    subject = "Activate Your Subscription"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [subscriber.email]

    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=html_message
        )
    except Exception as e:
        print(f"Error sending email: {str(e)}")  # Ideally, use logging instead



'''


def activate(request, uidb64, token):
    next_url = request.GET.get("next", "blog-home")  # Default to "blog-home"
    try:
        # Decode the user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Token is valid, activate the user
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        return redirect(next_url)  # Redirect to the specified next_url

    messages.error(request, "The activation link is invalid or expired.")
    raise Http404("Invalid activation link")

'''