from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


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
    image_profile = models.CharField(max_length=1000, default="")
    phone_number = models.CharField(max_length=25, default="")
    addressLine1 = models.CharField(max_length=100, default="")
    addressLine2 = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    bio = models.TextField(max_length=1000, default="")
    link1 = models.CharField(max_length=1000, default="")
    link2 = models.CharField(max_length=1000, default="")
    link3 = models.CharField(max_length=1000, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email


DEPARTMENT_CHOICES = (
    ('Computer Science', 'Computer Science'),
    ('Physics', 'Physics'),
    ('Math', 'Math'),
    ('English', 'English'),
    ('Engineering', 'Engineering'),
)


class Course(models.Model):
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='')
    course_number = models.CharField(max_length=20)
    course_name = models.CharField(max_length=50)
    credit_hours = models.IntegerField()

