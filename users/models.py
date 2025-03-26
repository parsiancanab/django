from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    is_subscribed = models.BooleanField(default=False) 
    subscriber_email = models.EmailField(blank=False, null=True)

    def __str__(self):
        return f"{self.user.username} - {'Subscribed' if self.is_subscribed else 'Not Subscribed'}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        img.thumbnail((300, 300))
        img.save(self.image.path)


class Event(models.Model):
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.date} at {self.time}"
    

