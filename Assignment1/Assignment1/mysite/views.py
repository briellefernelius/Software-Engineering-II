from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from users.models import Course
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
    item_list = Course.objects.all()
    context = {
        'item_list': item_list,
    }
    return render(request, 'mysite/main.html', context)


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
