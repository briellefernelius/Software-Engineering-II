from django import forms
from django.forms import ModelForm
from course.models import Course, Assignment


class CustomTimeField(forms.TimeField):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault('input_formats', ('%I:%M %p',))
    super(CustomTimeField, self).__init__(*args, **kwargs)


class CourseForm(ModelForm):
    choices = (('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('H', 'Thursday'), ('F', 'Friday'))
    meeting_time_days = forms.TypedMultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
    start_time = CustomTimeField()
    end_time = CustomTimeField()

    # for making the variable field 'meeting_time_days' not required
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meeting_time_days'].required = False

    class Meta:
        model = Course
        fields = ['department', 'course_number', 'course_name',  'credit_hours', 'meeting_time_days', 'start_time',
                  'end_time']


class StudentEnrollForm(ModelForm):
    class Meta:
        model = Course
        fields = ['department']


class AssignmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].required = False

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_points', 'submission_type']
