from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import date
from django.forms import ModelForm, Select, DateInput
from .models import *


class CustomDateField(forms.DateField):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault('input_formats', ("%m/%Y",))
    super(CustomDateField, self).__init__(*args, **kwargs)


class AccountForm(ModelForm):
    expiration_date = CustomDateField()

    class Meta:
        model = Account
        fields = ['cardholder_name', 'card_number', 'expiration_date', 'cvc_number']
