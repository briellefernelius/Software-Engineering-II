from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from django.forms import ModelForm, Select
from .models import Course


options = [('student', 'Student'), ('instructor', 'Instructor'), ]


class RegistrationForm(UserCreationForm):
    # email = forms.EmailField()
    birthday = forms.DateField()

    def clean_birthday(self):
        bday = self.cleaned_data['birthday']
        age = (date.today() - bday).days/362
        if age < 16:
            raise forms.ValidationError('Must be at least 16 years old to register')
        return bday

    def clean_username(self):
        mail = self.cleaned_data['username']

        special_characters = "@"

        if not any(c in special_characters for c in mail):
            raise forms.ValidationError('Username must be an email address')
        return mail

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'birthday']

    Status = forms.CharField(label='Are you a student or instructor?',
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}, choices=options))


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['department', 'course_number', 'course_name', 'credit_hours']


