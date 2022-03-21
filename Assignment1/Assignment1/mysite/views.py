import operator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
import datetime
from django.utils import timezone
from course.models import Course, CourseUser, Assignment, Submission
from users.models import CustomUser
from users.models import UserMessages
from users.forms import CreateMessageForm


@login_required
def home(request):
    return render(request, 'mysite/main.html')

@login_required
def main(request):

    item_list = request.session.get('courses')
    # if cookies don't load properly; re-makify them
    if item_list == None:
        return redirect(request, 'mysite/main.html')
    # Debug: cookie test
    print('courses cookie; item_list; main page: \t', item_list)

    courses_list = list()
    for course_id in item_list:
        courses_list.append(Course.objects.get(id=course_id))

    # get all assignments for the courses our user is enrolled in; order by due date
    assignment_list = Assignment.objects.all().filter(course__in=item_list).order_by('due_date').exclude(course__assignment__due_date__lte=datetime.datetime.utcnow())
    # get first 5 item


    # all the user's submissions
    submission_list = Submission.objects.all().filter(user_id=request.user.pk)
    print(f"SUBMISSION LIST: {submission_list}")
    slist = list()
    for item in submission_list:
        slist.append(item.assignment.id)
    print(f"slist: {slist}")
    assignment_list = assignment_list.exclude(id__in=slist)
    print(f"new assignment list = {assignment_list}")

    todolist = assignment_list[:5]
    # notifications list
    context = {'item_list': courses_list, 'todolist': todolist}
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary

    return render(request, 'mysite/main.html', context)


# this function will get called right after the user presses the login button
@login_required
def first_login(request):
    courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
    course_list = list()
    usercourse = list()
    for course in courseuser:
        course_list.append(course.course_id.pk)
        usercourse.append(course.id)

    request.session['courses'] = course_list
    request.session['courseuser'] = usercourse
    # v = request.session.get('courses')
    #v = request.session.get('courseuser')
    #print(f'cookies courseuser: {v}') # debug only
    return redirect('mysite:main')


@login_required
def register_classes(request):
    course_ids = request.session.get('courses')
    user = CustomUser.objects.get(pk=request.user.pk)
    user.tuition = request.POST.get('tuition')
    tuition = 0
    courses_list = list()  # Will be a list of course objects that the user is registered for
    for course_id in course_ids:
        courses_list.append(Course.objects.get(id=course_id))

    for course in courses_list:
        tuition += course.credit_hours * 100
    user.tuition = tuition
    user.save()

    item_list = Course.objects.all()
    title_name = request.GET.get('title_name')
    department = request.GET.get('department')
    if title_name != '' and title_name is not None:
        item_list = item_list.filter(course_name__icontains=title_name)
    if department != '' and department is not None:
        item_list = item_list.filter(department__icontains=department)

    context = {'item_list': item_list.exclude(pk__in=course_ids), 'usercourses': courses_list}
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary
    print(f'{user}, Registered classes: {courses_list}')  # For Unit Test
    return render(request, 'mysite/registerClasses.html', context)


def submission_all(request):
    # use database calls
    all_submissions = Submission.objects.all()
    # dictionary
    context = {'all_submissions': all_submissions}
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary
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
    context = {'submission' : submission}
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary
    return render(request, 'mysite/submission_details.html', context)
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

@login_required
def delete_message(request, message_id):
    message = UserMessages.objects.get(id=message_id)
    if message is not None:
        message.delete()
    # return to the webpage the user was at before messages
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def ignore_message(request, message_id):
    message = UserMessages.objects.get(id=message_id)
    if message is not None:

        if message.ignored is True:
            message.ignored = False

        elif message.ignored is False:
            message.ignored = True

        message.save()
    print(f'Message Ignored: {message.ignored}')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# This is a helper function. It will return a dictionary of all the current users messages.
# The idea is that this method can be called from anywhere and reduce duplicate code.
@login_required
def Get_Messages(request) -> dict:
    messages = UserMessages.objects.all().filter(user_id=request.user.pk)
    message_count = messages.exclude(ignored=True).count()
    context = {'messages': messages, 'message_count': message_count}
    return context


# A helper function to create a message and send it to the registered students in that course
@login_required
def Message_Students_In_Course(request, courseid, assignmentid = None, messageDescription = ""):
    registered_students = CourseUser.objects.all().filter(course_id=courseid)
    course = Course.objects.get(id=courseid)
    try:
        assignment = Assignment.objects.get(id=assignmentid)
    except ():
        print("Error in getting an assignment in 'Message_Students_In_Course' -> mysite\views.py")

    for student in registered_students:
        message = UserMessages()
        message.user_id = CustomUser.objects.get(id=student.user_id.id)
        if (messageDescription == ""):
            message.message_description = str(course.CourseName()) + ":\b" + str(course.instructor.get_full_name()) + " added an new assignment: " + str(assignment)
        else:
            message.message_description = messageDescription
        message.save()
        print(f"Messaging user -> {message.user_id}")
    return


# A helper function to create a message and send it to the registered students in that course
@login_required
def Message_Student_Submitted(request, submissionid, messageDescription = ""):

    submission = Submission.objects.get(id=submissionid)
    message = UserMessages()
    message.user_id = submission.user
    if (messageDescription == ""):
        message.message_description = submission.assignment.course.CourseName() + ":\t Assignment: " + submission.assignment.title + " was graded."
    else:
        message.message_description = messageDescription
    message.save()

    # debug
    # print(f"message: {message.message_description}")
    # print(f"Messaging user -> {message.user_id}")
    return