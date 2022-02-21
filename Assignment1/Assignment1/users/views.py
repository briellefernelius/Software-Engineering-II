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
from course.models import Course, CourseUser

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
        print(f"Users Courses: {user.courses}")
        return redirect('mysite:main')
    return render(request, 'users/login.html', { 'form': form })


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
    UserResult = item.filter(instructor=UserID)
    context = {
        "Courses": UserResult,
    }
    return render(request, 'users/calendar.html', context)


def display_image(request, id):
    return render(request, 'users/image-display.html', {'file_path': id})


def image(request):
    print(request.FILES)
    try:
        parent_obj = CustomUser.objects.get(id=request.user.pk)
    except:
        parent_obj = None
    if parent_obj is None:
        raise Http404

    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = parent_obj
        obj.save()
        # form = obj
        substring = "media/" + obj.url
        obj.url = substring
        print(obj.url)
        return render(request, 'users/image.html', {"form": form, "file_url": obj.url})
    return render(request, 'users/image.html', {"form": form})


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

