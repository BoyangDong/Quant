from django.contrib import admin
from django.urls import path, include, re_path
from marketdata import views

urlpatterns = [
    path('index/', views.display, name='index'),
    path('year-month/', views.year_month_form, name='year_month'),
]