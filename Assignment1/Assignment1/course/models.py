import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
from users.models import CustomUser

DEPARTMENT_CHOICES = (
    ('Computer Science', 'Computer Science'),
    ('Physics', 'Physics'),
    ('Math', 'Math'),
    ('English', 'English'),
    ('Engineering', 'Engineering'),
)


class Course(models.Model):
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='')
    course_number = models.CharField(max_length=8, validators=[MinLengthValidator(2)])
    course_name = models.CharField(max_length=50)
    credit_hours = models.IntegerField()

    meeting_time_days = models.CharField(max_length=200, default='')
    start_time = models.TimeField(default=datetime.time)
    end_time = models.TimeField(default=datetime.time)

    def __str__(self):
        return self.department + "-" + self.course_number + "-" + \
               str(CustomUser.objects.get(pk=self.instructor.id).get_full_name())

    def clean(self):
        if self.credit_hours < 0:
            raise ValidationError('Credit hours should be greater than 0')

        if self.start_time > self.end_time:
            raise ValidationError('Start time should be before end time')
        return super().clean()


class Submission(models.Model):
    file = models.FileField()


class Assignment(models.Model):
    title = models.CharField(max_length=50, default="", null=True)
    description = models.CharField(max_length=1000, default="", null=True)
    assignment_id = models.ForeignKey(Submission, on_delete=models.CASCADE, null=True)
    due_date = models.DateTimeField(default=datetime.time, null=True)
    max_points = models.IntegerField(default=0)
    points_received = models.IntegerField()
    file_type = models.CharField(max_length=10)
    is_graded = models.BooleanField(default=False)

    def clean(self):
        if self.max_points < 0:
            raise ValidationError("Maximum points should be 0 or greater!")

        if self.points_received < 0 or self.points_received > self.max_points:
            raise ValidationError("Points given should be greater than 0 and less than the maximum points!")

        return super().clean()
