import operator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
import datetime
from django.utils import timezone
from course.models import Course, CourseUser, Assignment
from users.models import CustomUser
from .models import *
from users.models import UserMessages
from django.conf import settings
import users
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from users.forms import CreateMessageForm


@login_required
def home(request):
    return render(request, 'mysite/main.html')

@login_required
def main(request):

    # item_list = CustomUser.objects.get(pk=request.user.pk).courses
    item_list = request.session.get('courses')
    courses_list = list()
    for course_id in item_list:
        courses_list.append(Course.objects.get(id=course_id))
    #
    # courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
    # item_list = list()
    # for course in courseuser:
    #     item_list.append(course.course_id)


    # get all assignments for the courses our user is enrolled in; order by due date
    assignment_list = Assignment.objects.all().filter(course__in=item_list).order_by('due_date').exclude(course__assignment__due_date__lte=datetime.datetime.utcnow())
    # get first 5 item
    todolist = assignment_list[:5]

    # notifications list
    messages = UserMessages.objects.all().filter(user_id=request.user.pk)

    print(f' UserMessages: {messages.exclude(ignored=False).count()}')
    print(f'!UserCourses: {courses_list}')

    context = {'item_list': courses_list, 'todolist': todolist, 'messages': messages, 'message_count': messages.exclude(ignored=True).count()}
    return render(request, 'mysite/main.html', context)


@login_required
def register_classes(request):
    course_ids = request.session.get('courses')

    courses_list = list()  # Will be a list of course objects that the user is registered for
    for course_id in course_ids:
        courses_list.append(Course.objects.get(id=course_id))

    item_list = Course.objects.all()
    title_name = request.GET.get('title_name')
    department = request.GET.get('department')
    if title_name != '' and title_name is not None:
        item_list = item_list.filter(course_name__icontains=title_name)
    if department != '' and department is not None:
        item_list = item_list.filter(department__icontains=department)


    context = {'item_list':  item_list.exclude(pk__in=course_ids), 'usercourses': courses_list}
    print(f'REgistered classes: {courses_list}')
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

@login_required
def create_message(request):
    form = CreateMessageForm(request.POST)
    if form.is_valid():
        message = UserMessages()
        message.user_id = CustomUser.objects.get(pk=request.user.pk)
        message.message_description = form.cleaned_data.get('message_description')
        message.save()
        return redirect('mysite:main')
    return render(request, 'users/message-form.html', {'form': form})

# This is for test purposes, can message every user.
# @login_required
# def create_message(request):
#     form = CreateMessageForm(request.POST)
#     if form.is_valid():
#         userss = CustomUser.objects.all()
#         for user in userss:
#             message = UserMessages()
#             message.user_id = CustomUser.objects.get(pk=user.pk)
#             message.message_description = form.cleaned_data.get('message_description')
#             message.save()
#         return redirect('mysite:main')
#     return render(request, 'users/message-form.html', {'form': form})


def delete_message(request, message_id):
    message = UserMessages.objects.get(id=message_id)
    if message is not None:
        message.delete()

    return redirect('mysite:main')

def ignore_message(request, message_id):
    message = UserMessages.objects.get(id=message_id)
    if message is not None:

        if message.ignored is True:
            message.ignored = False

        elif message.ignored is False:
            message.ignored = True

        message.save()
    print(f'Message Ignored: {message.ignored}')
    return redirect('mysite:main')

