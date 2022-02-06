import time

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import *
from django.utils import timezone
import datetime

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
    image_profile = models.ImageField(max_length=1000, default="", null=True)
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


DEPARTMENT_CHOICES = (
    ('Computer Science', 'Computer Science'),
    ('Physics', 'Physics'),
    ('Math', 'Math'),
    ('English', 'English'),
    ('Engineering', 'Engineering'),
)

DAY_OF_WEEK_CHOICES = (('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                       ('Thursday', 'Thursday'), ('Friday', 'Friday'))


class Course(models.Model):
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='')
    course_number = models.CharField(max_length=8, validators=[MinLengthValidator(2)])
    course_name = models.CharField(max_length=50)
    credit_hours = models.IntegerField()

    meeting_time_days = models.CharField(max_length=9, choices=DAY_OF_WEEK_CHOICES, default='')
    start_time = models.TimeField(default=datetime.time)
    end_time = models.TimeField(default=datetime.time)

    def __str__(self):
        return "PK: " + str(self.id) + " " + self.department + "-" + self.course_number + " Taught by " + str(
            CustomUser.objects.get(pk=self.instructor.pk).get_full_name())
