from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    subscription,
    subscribe
)
from . import views, email_utils

# Main URL patterns
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('vpcnb/', views.vpcnb, name='blog-vpcnb'),
    path('blog/', views.blog, name='blog-blog'),
    path('blogone/', views.blogone, name='blog-blogone'),
    path('blogtwo/', views.blogtwo, name='blog-blogtwo'),
    path('blogthree/', views.blogthree, name='blog-blogthree'),
    path('blogfour/', views.blogfour, name='blog-blogfour'),
    path('blog/datetime/', views.show_datetime, name='show_datetime'),
    path('plan/', views.plan, name='blog-plan'),
    path('subscribe/', subscribe, name='subscribe'),
    path('subscription/', subscription, name='subscription'),
    path('activate/<str:uidb64>/<str:token>/', email_utils.activate, name='activate'),
]

