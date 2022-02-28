from django.contrib import admin

# Register your models here.
from course.models import *

admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(CourseUser)
