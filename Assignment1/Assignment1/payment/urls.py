from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'payment'

urlpatterns = [
    path('account/', views.account, name="account"),
]
