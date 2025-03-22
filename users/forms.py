from django import forms
from blog.models import Subscriber
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Event


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['firstname', 'lastname', 'phone', 'email']
        labels = {
            'email': 'ایمیل',
            'firstname': 'نام',
            'lastname': 'نام خانوادگی',
            'phone': 'تلفن'
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['firstname', 'lastname', 'phone', 'email']
        labels = {
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'email': 'E-mail',
            'phone': 'Phone'
        }
 

        
  
    
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'time']