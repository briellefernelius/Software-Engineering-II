from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'payment'

urlpatterns = [
    path('account/', views.account, name="account"),
    path('amount_fail/', views.amount_fail, name="amount_fail"),
    path('payment_success/', views.payment_success, name="payment_success"),
    path('card_decline/', views.card_decline, name="card_decline"),
]
