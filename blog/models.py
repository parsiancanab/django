from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})



class Subscription(models.Model):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=100, blank=True, default='')  
    lastname = models.CharField(max_length=100, blank=True, default='')  
    phone = models.PositiveBigIntegerField(unique=True, blank=True, null=True)  
    subscribed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=255, blank=True, null=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.email}, {self.phone or 'N/A'}, {self.full_name} ({self.subscribed_date_str})"
   
    @property
    def full_name(self):
        if self.firstname and self.lastname:
            return f"{self.firstname} {self.lastname}"
        return self.firstname or self.lastname or 'N/A'

    @property
    def subscribed_date_str(self):
        return self.subscribed_date.strftime('%Y-%m-%d %H:%M:%S')


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscriber', null=True, blank=True)
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=100, blank=True, default='')  
    lastname = models.CharField(max_length=100, blank=True, default='')  
    phone = models.PositiveBigIntegerField(unique=True, blank=True, null=True)  
    subscribed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=255, blank=True, null=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #subscribed_at = models.DateTimeField(auto_now_add=True, default=timezone.now)


    def __str__(self):
        return f"{self.email}, {self.phone or 'N/A'}, {self.full_name} ({self.subscribed_date_str})"
   
    @property
    def full_name(self):
        if self.firstname and self.lastname:
            return f"{self.firstname} {self.lastname}"
        return self.firstname or self.lastname or 'N/A'

    @property
    def subscribed_date_str(self):
        local_time = timezone.localtime(self.subscribed_date)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
    #    return self.subscribed_date.strftime('%Y-%m-%d %H:%M:%S')


