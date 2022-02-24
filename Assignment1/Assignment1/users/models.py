import pathlib
import time
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import *
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
from django.conf import settings


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email bust be set')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_instructor', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    birthday = models.DateField(null=True, blank=True)
    is_instructor = models.BooleanField(default=False)
    image_profile = models.ImageField(max_length=1000, default="", upload_to='profile_pics/', blank=True)
    phone_number = models.CharField(max_length=13, default="", null=True, validators=[MinLengthValidator(10)])
    addressLine1 = models.CharField(max_length=100, default="", null=True)
    addressLine2 = models.CharField(max_length=100, default="", null=True)
    city = models.CharField(max_length=100, default="", null=True)
    bio = models.TextField(max_length=1000, default="", null=True)
    link1 = models.CharField(max_length=1000, default="", null=True)
    link2 = models.CharField(max_length=1000, default="", null=True)
    link3 = models.CharField(max_length=1000, default="", null=True)
    courses = list()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return "User: " + str(self.id) + " " + self.email + " | " + self.first_name + " " + self.last_name

    # Takes a courseuser list of objects as courseuser_list, and the id of the course to compare against
    def isRegisteredTo(self, courseuser_list, course_id) -> bool:
        try:
            is_registered = False
            for course in courseuser_list:
                if course_id == course.id:
                    is_registered = True
            return is_registered

        except Exception:
            print("There was an error in the isRegisteredTo function of the CustomUser class in users/models.py")
            return False


def user_image_upload_handler(instance, filename):
    print("instance:" + str(instance.user.pk))
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1())  # uuid1 -> uuid + timestamps
    instance.url = f"profile_pics/{instance.user.pk}/{new_fname}{fpath.suffix}"
    return f"profile_pics/{instance.user.pk}/{new_fname}{fpath.suffix}"


class UserImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_image_upload_handler)
    url = models.CharField(max_length=1000, default="", null=True)

    def __str__(self):
        return str(self.user)
