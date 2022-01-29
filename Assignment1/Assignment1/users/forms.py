from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


options = [('student', 'Student'),
         ('instructor', 'Instructor'),]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    birthday = forms.DateField(help_text='Required. Format: DD-MM-YYYY')

    Status = forms.CharField(label='Are you a student or instructor?', widget = forms.RadioSelect(choices = options))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'birthday']
