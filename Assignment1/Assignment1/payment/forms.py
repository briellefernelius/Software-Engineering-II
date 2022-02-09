from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import date
from django.forms import ModelForm, Select
from .models import *


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['cardholder_name', 'card_number', 'expiration_date', 'cvc_number']
