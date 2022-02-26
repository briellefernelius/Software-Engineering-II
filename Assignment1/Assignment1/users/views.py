import os
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage, default_storage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.views.decorators.vary import vary_on_cookie
from .forms import *
from .models import *
from django.http import HttpResponse, Http404
from course.models import Course, CourseUser, Assignment

User = get_user_model()


@login_required
@vary_on_cookie
def login(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        # get the CourseUser object associated with the user's pk.
        courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
        user = CustomUser.objects.get(pk=request.user.pk)
        # make a list, then add each course to that list from the CourseUser's course_id field
        for obj in courseuser:
            try:
                # try and remove the course from their course list
                user.courses.remove(obj)
            except ValueError:
                # if the course is not already in their course list, then add it
                user.courses.append(obj.course_id)
        # print(f"Users Courses: {user.courses}")
        return redirect('mysite:main')
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    try:
        item_list = CustomUser.objects.all()
        return render(request, 'users/profile.html', {'item_list': item_list})
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
        return render(request, 'users/profile-form.html', {'form': form, 'item': item})


# @login_required
def calendar(request):
    UserID = request.user.id
    item = Course.objects.all()
    LoggedUser = User.objects.get(id=UserID)
    Assignment_list = []
    if LoggedUser.is_instructor: # is instructor
        UserResult = item.filter(instructor_id=UserID) # get instructor courses
    else: # is student; get student courses
        course_list = Course.objects.all()
        registered_list = []
        # Loop through all courses. If the user is registered in that course append to list of register courses.
        for course in list(course_list):
            if (LoggedUser.isRegisteredTo(LoggedUser.courses, course.id) == True):
                registered_list.append(course)
        UserResult = registered_list
        # get all the assignment for the user (student)
        c_list = LoggedUser.courses
        asn_list = Assignment.objects.all()
        a_list = []
        for asn in asn_list:
            if asn.course in c_list:
                a_list.append(asn)
        Assignment_list = a_list
        # DO NOT remove for DEBUG purposes.
    #print('AL:\t',Assignment_list)
    #print('UR\t',UserResult)
    context = {
        "Courses": UserResult,
        "Assignment": Assignment_list,
    }
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
