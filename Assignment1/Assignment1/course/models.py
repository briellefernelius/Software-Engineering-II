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
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        from users.models import CustomUser
        return str(self.pk) + " " + self.department + "-" + self.course_number + "-" + \
               str(CustomUser.objects.get(pk=self.instructor.id).get_full_name())

    def ConvertDaysToInts(self) -> list[int]:
        # returns a list of integers that represent the days as a list of ints
        array = self.meeting_time_days
        print(array)
        array = array.replace("'", "")
        array = array.replace("[", "")
        array = array.replace("]", "")
        array = array.replace(",", "")
        print(array)
        array = array.replace('M', "1")
        array = array.replace('T', "2")
        array = array.replace('W', "3")
        array = array.replace('H', "4")
        array = array.replace('F', "5")

        array = array.replace('h', '')
        array = array.replace(' ', '')

        intarray = [int(i) for i in array]
        print(f"Array: {intarray}")
        return intarray

    def clean(self):
        if self.credit_hours < 0:
            raise ValidationError('Credit hours should be greater than 0')

        if self.start_time > self.end_time:
            raise ValidationError('Start time should be before end time')

        if self.credit_hours != 0 and self.meeting_time_days is None:
            raise ValidationError('Must choose meeting days')

        return super().clean()


class Submission(models.Model):
    file = models.FileField()


SUBMISSION_CHOICES = (('.file', 'File'), ('text', "Text"))


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50, default="", null=True)
    description = models.CharField(max_length=1000, default="", null=True)
    submission_id = models.ForeignKey(Submission, on_delete=models.CASCADE, null=True)
    due_date = models.DateTimeField(default=datetime.time, null=True)
    max_points = models.IntegerField(default=0)
    points_received = models.IntegerField(default=0, null=True)
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_CHOICES, null=True)
    is_graded = models.BooleanField(default=False)

    def clean(self):
        if self.max_points < 0:
            raise ValidationError("Maximum points should be 0 or greater!")

        if self.points_received < 0 or self.points_received > self.max_points:
            raise ValidationError("Points given should be greater than 0 and less than the maximum points!")

        return super().clean()


# This class is needed so a user can have multiple courses they are signed up for :)
class CourseUser(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk) + " " + self.user_id.first_name + " - " + self.course_id.course_name
