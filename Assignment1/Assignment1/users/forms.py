from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import date
from django.forms import ModelForm, Select
from .models import *


class RegistrationForm(UserCreationForm):
    bool_choices = ((1, 'Instructor'), (0, 'Student'))

    is_instructor_or_student = forms.TypedChoiceField(
        choices=bool_choices, widget=forms.RadioSelect, coerce=int
    )

    def clean_birthday(self):
        bday = self.cleaned_data['birthday']
        age = (date.today() - bday).days / 362
        if age < 16:
            raise forms.ValidationError('Must be at least 16 years old to register')
        return bday

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'birthday', 'is_instructor_or_student']


class ImageForm(forms.ModelForm):

    class Meta:
        model = UserImage
        fields = ['image']


class ProfileEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_profile'].required = False
        self.fields['phone_number'].required = False
        self.fields['addressLine1'].required = False
        self.fields['addressLine2'].required = False
        self.fields['city'].required = False
        self.fields['bio'].required = False
        self.fields['link1'].required = False
        self.fields['link2'].required = False
        self.fields['link3'].required = False

    class Meta:
        model = CustomUser
        fields = ['image_profile', 'first_name', 'last_name', 'phone_number', 'birthday', 'addressLine1', 'addressLine2', 'city', 'bio',
                  'link1', 'link2', 'link3']


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class AdminUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_profile'].required = False
        self.fields['phone_number'].required = False
        self.fields['addressLine1'].required = False
        self.fields['addressLine2'].required = False
        self.fields['city'].required = False
        self.fields['bio'].required = False
        self.fields['link1'].required = False
        self.fields['link2'].required = False
        self.fields['link3'].required = False

    class Meta:
        model = CustomUser
        fields = ('email',)


class EditProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_profile'].required = False
        self.fields['phone_number'].required = False
        self.fields['addressLine1'].required = False
        self.fields['addressLine2'].required = False
        self.fields['city'].required = False
        self.fields['bio'].required = False
        self.fields['link1'].required = False
        self.fields['link2'].required = False
        self.fields['link3'].required = False

    class Meta:
        model = CustomUser
        fields = ['image_profile', 'first_name', 'last_name', 'birthday', 'phone_number', 'addressLine1',
                  'addressLine2', 'city', 'bio', 'link1', 'link2', 'link3']


class CreateMessageForm(ModelForm):
    class Meta:
        model = UserMessages
        fields = ['message_description']
