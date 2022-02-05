from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.views.decorators.vary import vary_on_cookie
from .forms import *
from .models import *
from django.http import HttpResponse

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
    item_list = User.objects.filter(user=request.user)
    context = {
        'item_list': item_list,
    }
    return render(request, 'users/profile.html', context)


def profile_edit(request, id):
    item = User.objects.get(id=id)
    form = ProfileForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('users:profile')

    return render(request, 'users/profile-form.html', {'form': form, 'item': item})


def calendar(request):
    return render(request, 'users/calendar.html')


def image(request):
    return render(request, 'users/image.html')


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




