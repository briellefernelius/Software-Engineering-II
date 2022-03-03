from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'payment'

urlpatterns = [
    path('account/', views.account, name="account"),
    path('paymentSuccess/', views.PaymentView.as_view(), name="payment_success"),
    path('paymentFail/', views.PaymentView.as_view(), name="payment_fail"),
]
