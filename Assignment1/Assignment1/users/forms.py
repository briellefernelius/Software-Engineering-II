from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date


options=[('student', 'Student'),
         ('instructor', 'Instructor'),]

class RegistrationForm(UserCreationForm):
    #email = forms.EmailField()
    birthday = forms.DateField()

    Status = forms.CharField(label='Are you a student or instructor?', widget = forms.RadioSelect(choices = options))

    def clean_birthday(self):
        bday = self.cleaned_data['birthday']
        age = (date.today() - bday).days/362
        if age < 16:
            raise forms.ValidationError('Must be at least 16 years old to register')
        return bday

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'birthday']
