from django.db.models import Sum
from course.models import Course, CourseUser
from users.models import CustomUser
from django.shortcuts import render, redirect
from .forms import *
from .models import *

# Create your views here.


def account(request):
    courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
    item_list = list()
    tuition = 0
    form = AccountForm(request.POST or None)
    if form.is_valid():
        form.save()
    for course in courseuser:
        tuition += course.course_id.credit_hours * 100
    print(f"CustomUser.courses = {item_list}")
    return render(request, 'payment/account.html', {'item_list': item_list, 'form': form, 'tuition': tuition})

