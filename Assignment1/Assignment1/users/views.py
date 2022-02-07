from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.views.decorators.vary import vary_on_cookie
from .forms import *
from .models import *
from django.http import HttpResponse, Http404

User = get_user_model()


@login_required
@vary_on_cookie
def login(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        return redirect('mysite:main')
    return render(request, 'users/login.html', {
        'form': form
    })


@login_required
def profile(request):
    try:
        item_list = User.objects.all()
        return render(request, 'users/profile.html', {'item_list': item_list})
    except User.DoesNotExist:
        return render(request, 'users/home.html')


def profile_edit(request, id):
    item = User.objects.get(id=id)
    form = EditProfileForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('users:profile')

    return render(request, 'users/profile-form.html', {'form': form, 'item': item})


def calendar(request):
    return render(request, 'users/calendar.html')


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


def courses(request):
    item_list = Course.objects.all()
    context = {
        'item_list': item_list,
    }
    return render(request, 'users/courses.html', context)


def courses_add(request):
    form = CourseForm(request.POST or None)

    if form.is_valid():
        # For adding the course
        course = Course()
        course.department = request.POST.get('department')
        course.course_name = request.POST.get('course_name')
        course.course_number = request.POST.get('course_number')
        course.credit_hours = request.POST.get('credit_hours')
        course.start_time = request.POST.get('start_time')
        course.end_time = request.POST.get('end_time')
        course.instructor = CustomUser.objects.get(pk=request.user.pk)
        course.save()
        # For attaching the course to the user
        CustomUser.objects.get(pk=request.user.pk).courses.append(course)
        form.save()
        return redirect('users:courses')
    return render(request, 'users/courses-form.html', {'form': form})


def courses_delete(request, id):
    item = Course.objects.get(id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('users:courses')
    return render(request, 'users/courses-delete.html', {'item': item})


def courses_edit(request, id):
    item = Course.objects.get(id=id)
    form = CourseForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('users:courses')

    return render(request, 'users/courses-form.html', {'form': form, 'item': item})


def courses_enroll(request, id):
    CustomUser.objects.get(pk=request.user.pk).courses.append(Course.objects.get(id=id))
    return redirect('mysite:main')

    # return render(request, 'users/courses-form.html', {'form': form, 'item': item})
