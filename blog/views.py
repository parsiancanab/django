import secrets
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from datetime import datetime
from calendar import HTMLCalendar
from .email_utils import send_activation_email
from django.shortcuts import redirect, render
from .models import Post, Subscriber, Subscription 
from users.forms import SubscribeForm, SubscriptionForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.models import Profile

# Home View
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

# Class-based Views for Posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        return self.request.user == self.get_object().author

# Static Pages
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def vpcnb(request):
    return render(request, 'blog/vpcnb.html', {'title': 'vpcnb'})

def plan(request):
    return render(request, 'blog/plan.html', {'title': 'Plan'})

# Blog Pages
def blog(request):
    return render(request, 'blog/blog.html', {'title': 'Blog'})

def blogone(request):
    return render(request, 'blog/blogone.html', {'title': 'Blogone'})

def blogtwo(request):
    return render(request, 'blog/blogtwo.html', {'title': 'Blogtwo'})

def blogthree(request):
    return render(request, 'blog/blogthree.html', {'title': 'Blogthree'})

def blogfour(request):
    return render(request, 'blog/blogfour.html', {'title': 'Blogfour'})


def blog_detail(request, blog_id):
    return render(request, f'blog/blog{blog_id}.html', {'title': f'Blog {blog_id}'})

# Calendar Views
def show_datetime(request):
    current_time = datetime.now().time()
    current_date = datetime.now().date()
    calendar_html = HTMLCalendar().formatmonth(current_date.year, current_date.month)
    return render(request, 'blog/base.html', {
        'current_time': current_time,
        'current_date': current_date,
        'calendar_html': calendar_html
    })


# Subscriber List
def subscriber_list(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'users/subscriber_list.html', {'subscribers': subscribers})


def generate_activation_token(subscriber):
    # Example: Generate and save a token to the subscriber
    token = secrets.token_urlsafe(32)
    subscriber.activation_token = token
    subscriber.save()
    return token


def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            firstname, lastname, phone, email = (
                cleaned_data["firstname"],
                cleaned_data["lastname"],
                cleaned_data["phone"],
                cleaned_data["email"],
            )

            try:
                # Create or get user
                user, user_created = User.objects.get_or_create(
                    username=email,
                    defaults={"first_name": firstname, "last_name": lastname, "email": email}
                )
                # Create or get subscriber
                subscriber, created = Subscriber.objects.get_or_create(
                    email=email,
                    defaults={"firstname": firstname, "lastname": lastname, "phone": phone}
                )

                # If subscriber was retrieved (not created), update missing fields
                if not created:
                    updated_fields = []
                    if not subscriber.firstname:
                        subscriber.firstname = firstname
                        updated_fields.append("firstname")
                    if not subscriber.lastname:
                        subscriber.lastname = lastname
                        updated_fields.append("lastname")
                    if not subscriber.phone:
                        subscriber.phone = phone
                        updated_fields.append("phone")
                    
                    if updated_fields:
                        subscriber.save(update_fields=updated_fields)

                # Send activation email only if the user was newly created
                if user_created:
                    send_activation_email(request, subscriber, next_url="blog-home")  # Pass next_url

                messages.success(request, f"{firstname}, please check your email to activate your subscription.")
                return redirect("blog-home")  # Redirect to "blog-home"

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    else:
        form = SubscribeForm()

    return render(request, "blog/subscribe.html", {"form": form})


def subscription(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            firstname, lastname, phone, email = (
                cleaned_data["firstname"],
                cleaned_data["lastname"],
                cleaned_data["phone"],
                cleaned_data["email"],
            )

            try:
                # Create or get user
                user, user_created = User.objects.get_or_create(
                    username=email,
                    defaults={"first_name": firstname, "last_name": lastname, "email": email}
                )
                # Create or get subscriber
                subscriber, created = Subscription.objects.get_or_create(
                    email=email,
                    defaults={"firstname": firstname, "lastname": lastname, "phone": phone}
                )

                # If subscriber was retrieved (not created), update missing fields
                if not created:
                    updated_fields = []
                    if not subscriber.firstname:
                        subscriber.firstname = firstname
                        updated_fields.append("firstname")
                    if not subscriber.lastname:
                        subscriber.lastname = lastname
                        updated_fields.append("lastname")
                    if not subscriber.phone:
                        subscriber.phone = phone
                        updated_fields.append("phone")
                    
                    if updated_fields:
                        subscriber.save(update_fields=updated_fields)

                # Send activation email only if the user was newly created
                if user_created:
                    send_activation_email(request, subscriber, next_url="blog-blog")  # Pass "blog-blog"

                messages.success(request, f"{firstname}, please check your email to activate your subscription.")
                return redirect("blog-blog")  # Redirect to "blog-blog"

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    else:
        form = SubscriptionForm()

    return render(request, "blog/subscription.html", {"form": form})


def subscribe_user(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        profile.is_subscribed = True
        profile.subscriber_email = request.user.email  # Use their email or ask for input
        profile.save()
        return redirect("success_page")
    return redirect("login")