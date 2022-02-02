from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# For future, assignment submission
class Submission(models.Model):
    # assignment_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=250)
    file_type = models.CharField(max_length=10)
    is_graded = models.BooleanField(default=False)

    def __str__(self):
        return self.assignment_name + " \n" + self.file_type + "\nGraded: " + str(self.is_graded) + "\n"


