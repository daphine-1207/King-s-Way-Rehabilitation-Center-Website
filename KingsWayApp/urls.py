from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('donate/', views.donate, name='donate'),
    path('shop/', views.shop, name='shop'),
    path('success/', success_view, name='success'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),
 
]
