from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile
from blog.models import Subscriber, Subscription

# Ensure compatibility with custom User models
User = get_user_model()

# Register Profile model
admin.site.register(Profile)

# Register Subscriber model (if not already registered)
if admin.site.is_registered(Subscriber):
    admin.site.unregister(Subscriber)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "email", "phone", "subscribed_date")
    search_fields = ("email", "firstname", "lastname", "phone")


# Register Subscription model (if not already registered)
if admin.site.is_registered(Subscription):
    admin.site.unregister(Subscription)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "email", "phone", "subscribed_date")
    search_fields = ("email", "firstname", "lastname", "phone")


# Define an inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fields = ("is_subscribed", "subscriber_email")  # Only relevant fields


# Extend the existing UserAdmin instead of re-registering
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "get_subscription_status")
    search_fields = ("username", "email", "first_name", "last_name")  # Added search fields

    def get_subscriber_email(self, obj):
        """Return the email of the associated Subscriber, if available."""
        subscriber = Subscriber.objects.filter(user=obj).first()
        return subscriber.email if subscriber else "Not Subscribed"

    get_subscriber_email.short_description = "Subscriber Email"

    def get_subscription_status(self, obj):
        """Check if the user has an associated profile and return subscription status."""
        return "Subscribed" if hasattr(obj, "profile") and obj.profile.is_subscribed else "Not Subscribed"

    get_subscription_status.short_description = "Subscription Status"


# Unregister and register the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)




'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, User
from django.contrib.auth import get_user_model
from .models import Profile
from blog.models import Subscriber, Subscription

User = get_user_model()  # Ensure compatibility with custom User models

# Register Profile model
admin.site.register(Profile)

# Ensure Subscriber is registered only once
if admin.site.is_registered(Subscriber):
    admin.site.unregister(Subscriber)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phone', 'subscribed_date')
    search_fields = ('email', 'firstname', 'lastname', 'phone')


if admin.site.is_registered(Subscription):
    admin.site.unregister(Subscription)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phone', 'subscribed_date')
    search_fields = ('email', 'firstname', 'lastname', 'phone')


# Define an inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fields = ("is_subscribed", "subscriber_email")



# Extend the existing UserAdmin instead of re-registering
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "get_subscription_status")
    # list_display = UserAdmin.list_display + ('get_subscriber_email',)

    def get_subscriber_email(self, obj):
        # First check if the user has an associated Subscriber
        subscriber = Subscriber.objects.filter(user=obj).first()
        if subscriber:
            return subscriber.email
        return "Not Subscribed"

    get_subscriber_email.short_description = "Subscriber Email"

    
    def get_subscription_status(self, obj):
            if hasattr(obj, 'profile') and obj.profile:
                return "Subscribed" if obj.profile.is_subscribed else "Not Subscribed"
            return "Not Subscribed"  # Return default if profile is missing
    get_subscription_status.short_description = "Subscription Status"




# Unregister and then register the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)''
''
'''