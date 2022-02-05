from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    userstatus = models.CharField(max_length=20, default="active")
    image_profile = models.ImageField(upload_to='images', default='images/non/noimg.jpg')
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=25, default="")
    addressLine1 = models.CharField(max_length=100, default="")
    addressLine2 = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    bio = models.TextField(max_length=1000, default="")
    link1 = models.CharField(max_length=1000, default="")
    link2 = models.CharField(max_length=1000, default="")
    link3 = models.CharField(max_length=1000, default="")

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

