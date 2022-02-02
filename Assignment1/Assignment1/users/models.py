from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    userstatus = models.CharField(max_length=20, default="active")
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
