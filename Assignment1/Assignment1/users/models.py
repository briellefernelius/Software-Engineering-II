from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #birthday = models.DateField()
    birthday = models.DateField()
    userstatus = models.CharField(max_length=20, default="active")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email_address = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    address_line1 = models.CharField(max_length=1024, blank=True)
    address_line2 = models.CharField(max_length=1024, blank=True)
    city = models.CharField(max_length=1024, blank=True)

    image_profile = models.ImageField(upload_to='images', default='images/non/noimg.jpg')

    def __str__(self):
        return self.user.username + " - " + self.birthday.strftime('%m/%d/%Y')


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
