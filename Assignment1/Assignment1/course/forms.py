from django import forms
from django.forms import ModelForm
from course.models import Course, Assignment


class CourseForm(ModelForm):

    choices = (('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('Th', 'Thursday'), ('F', 'Friday'))
    meeting_time_days = forms.TypedMultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Course
        fields = ['department', 'course_number', 'course_name',  'credit_hours', 'meeting_time_days', 'start_time', 'end_time']


class StudentEnrollForm(ModelForm):
    class Meta:
        model = Course
        fields = ['department']

class AssignmentForm(ModelForm):

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_points']