from urllib import request

from importlib._common import _
from users.models import CustomUser
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import date
from django.forms import ValidationError
from django.forms import ModelForm, Select, DateInput
from urllib3.connectionpool import xrange
import re
from datetime import date
from calendar import monthrange, IllegalMonthError
from django import forms
from django.conf import settings
from .models import *


MONTH_FORMAT = getattr(settings, 'MONTH_FORMAT', '%b')
VERIFICATION_VALUE_RE = r'^([0-9]{3,4})$'
CREDIT_CARD_RE = r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3' \
                 r'(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\d{11})$'


class VerificationValueField(forms.CharField):
    """
    Form field that validates credit card verification values (e.g. CVV2).
    See http://en.wikipedia.org/wiki/Card_Security_Code
    """

    widget = forms.TextInput(attrs={'maxlength': 4})
    default_error_messages = {
        'required': _(u'Please enter the three- or four-digit verification code for your credit card.'),
        'invalid': _(u'The verification value you entered is invalid.'),
    }

    def clean(self, value):
        value = value.replace(' ', '')
        if not value and self.required:
            raise forms.ValidationError('Please enter the three- or four-digit verification code for your credit card.')
        if value and not re.match(VERIFICATION_VALUE_RE, value):
            raise forms.ValidationError('The verification value you entered is invalid.')
        return value


class AccountForm(ModelForm):
    cvc_number = VerificationValueField()

    class Meta:
        model = Account
        fields = ['cardholder_name', 'card_number', 'expiration_month', 'expiration_year', 'cvc_number', 'amount']
