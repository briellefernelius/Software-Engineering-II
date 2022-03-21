import os
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage, default_storage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.vary import vary_on_cookie
from .forms import *
from .models import *
from django.http import HttpResponse, Http404
from course.models import Course, CourseUser, Assignment
from Assignment1 import settings
from mysite.views import Get_Messages

User = get_user_model()

# def login(request):
#     form = AuthenticationForm(data=request.POST or None)
#     if form.is_valid():
#     # get the CourseUser object associated with the user's pk.
#         courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
#         course_list = list()
#         for course in courseuser:
#             course_list.append(course.course_id.pk)
#
#         request.session['courses'] = course_list
#         v = request.session.get('courses')
#         print(f'cookies: {v}')
#         return redirect('mysite:main')
#
#     return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    try:
        item_list = CustomUser.objects.all()
        context = {'item_list': item_list}
        messages = Get_Messages(request)
        context.update(messages)  # merging the context dictionary with the messages dictionary
        return render(request, 'users/profile.html', context)
    except CustomUser.DoesNotExist:
        return render(request, 'users/home.html')


def profile_edit(request, id):
    item = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            if request.FILES.get('image_profile', None) != None:
                try:
                    os.remove(request.user.image_profile.url)
                except Exception as e:
                    print('Exception in removing old profile image: ', e)
                request.user.image_profile = request.FILES['image_profile']
                request.user.save()
            return redirect('users:profile')
    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form, 'item': item}
        messages = Get_Messages(request)
        context.update(messages)  # merging the context dictionary with the messages dictionary
        return render(request, 'users/profile-form.html', context)


@login_required
def calendar(request):
    UserID = request.user.id
    item = Course.objects.all()
    LoggedUser = User.objects.get(id=UserID)
    assignment_list = []
    v = request.session.get('courses')
    print(f'courses cookie: calendar view\t: {v}')      # Unit Testing
    UserResult = []
    if LoggedUser.is_instructor: # is instructor
        UserResult = item.filter(instructor_id=UserID) # get instructor courses
    else: # is student; get student courses

        # loop through the stored courses cookie
        course_list = request.session.get('courses')

        for course_id in course_list:
            UserResult.append(Course.objects.get(id=course_id))
            print(f'courses cookie: calendar view\t: {UserResult}')  # Unit Testing

        # get all the assignment for the user (student)
        asn_list = Assignment.objects.all()
        for asn in asn_list:
            for ur_course in UserResult:
                if asn.course == ur_course:
                    assignment_list.append(asn)
        # DO NOT remove for DEBUG purposes.
    #print('AL:\t',Assignment_list)
    context = {
        "Courses": UserResult,
        "Assignment": assignment_list,
    }
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary
    return render(request, 'users/calendar.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')

            messages.success(request, f'Registration Successful {firstname} {lastname}!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def pieChart(request):
    return render(request, 'users/pieChart.html')
