from django.contrib import admin
from django import forms
from .models import Post ,Subscription, Subscriber # Import the model
from django.utils import timezone

admin.site.site_header = "My PCNB Admin"
admin.site.site_title = "PCNB Admin Portal"
admin.site.index_title = "Welcome to PCNB Administration"


admin.site.register(Post)
admin.site.register(Subscription)
admin.site.register(Subscriber)


# Custom Form for Post Model
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'  # Include all fields


# Custom Admin Class
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('field1', 'field2', 'created_at')  # List view columns
    search_fields = ('field1', 'field2')  # Searchable fields
    list_filter = ('status', 'created_at')  # Sidebar filters
    ordering = ('-created_at',)  # Default sorting
    readonly_fields = ('created_at',)  # Non-editable fields
    
    def has_delete_permission(self, request, obj=None):
        return False  # Disable delete option



class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'subscribed_date_display')
    
    def subscribed_date_display(self, obj):
        # Convert the UTC time to local time
        local_time = timezone.localtime(obj.subscribed_date)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
    subscribed_date_display.admin_order_field = 'subscribed_date'  # Allows ordering by the original field
    subscribed_date_display.short_description = 'Subscribed Date'  # Column title in admin
    
# admin.site.register(Subscriber, SubscriberAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'phone', 'subscribed_date_display')
    
    def subscribed_date_display(self, obj):
        # Convert the UTC time to local time
        local_time = timezone.localtime(obj.subscribed_date)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
    subscribed_date_display.admin_order_field = 'subscribed_date'  # Allows ordering by the original field
    subscribed_date_display.short_description = 'Subscribed Date'  # Column title in admin