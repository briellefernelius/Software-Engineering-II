import operator

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
import datetime
from django.utils import timezone

from course.models import Course, CourseUser, Assignment
from users.models import CustomUser
from .models import *
from django.conf import settings
import users
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage


@login_required
def home(request):
    return render(request, 'mysite/home.html')


@login_required
def main(request):

    # item_list = CustomUser.objects.get(pk=request.user.pk).courses
    courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
    item_list = list()
    for course in courseuser:
        item_list.append(course.course_id)

    # get all assignments for the courses our user is enrolled in; order by due date
    assignment_list = Assignment.objects.all().filter(course__in=item_list).order_by('due_date')
    assignment_list.exclude(due_date__lt=timezone.now())
    # compare and sort assignments; grab the next five that are due.
    # make sure that they are in chronological order
    #for assignment in assignment_list:
        # remove old assignments from the assignment list; only grab current/future
    #    if assignment.due_date >= timezone.now():
    #        current_assignment_list.append(assignment)
    # get first 5 item
    assignment_list_first_5 = assignment_list[:5]

    print(f"CustomUser.courses =  {item_list}")
    return render(request, 'mysite/main.html', {'item_list': item_list, 'assignment_list': assignment_list_first_5})


@login_required
def register_classes(request):
    item_list = Course.objects.all()
    context = {
        'item_list': item_list,
    }
    return render(request, 'mysite/registerClasses.html', context)


def submission_all(request):
    # use database calls
    all_submissions = Submission.objects.all()
    # dictionary
    context = {'all_submissions': all_submissions}
    # html = '<br><br><br>'
    # for submission in all_submissions:
    #     url = 'main/submission/' + str(submission.id) + '/'
    #     html += '<a href="' + url + '">' + submission.assignment_name + '</a><br>'
    return render(request, 'mysite/submission.html', context)


# need to update to return a page that displays the results
def submission_with_id(request, submission_id):
    try:
        submission = Submission.objects.get(pk=submission_id)
    except Submission.DoesNotExist:
        raise Http404("Submission id does not exist")
    return render(request, 'mysite/submission_details.html', {'submission' : submission})
    # return HttpResponse("<h2>Successful: " + str(submission_id) + "</h2>")


def submission_graded(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    try:
        selected_submission = submission.get(pk=request.POST['submission_id'])
    except (KeyError, Submission.DoesNotExist):
        return render(request, 'mysite/submission_details.html',
            {'submission': submission, 'error_message': "You did not select a valid submission"},)
    else:
        selected_submission.is_graded = True
        selected_submission.save()
        return render(request, 'mysite/submission_details.html', {'submission': submission})
