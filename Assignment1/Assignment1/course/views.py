from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from course.forms import CourseForm, AssignmentForm

# Create your views here.
from users.models import CustomUser
from course.models import Course

User = get_user_model()

global user_selected_courses

def course_page(request, id):
    course = Course.objects.get(pk=id)
    context = {
        'course': course
    }
    return render(request, 'course/course_page.html', context)


def courses(request):
    item_list = Course.objects.all()
    context = {
        'item_list': item_list,
    }
    return render(request, 'course/courses.html', context)


def assigment_add(request):

    form = AssignmentForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('course:courses')
    return render(request, 'course/assignment-form.html', {'form': form})


def courses_add(request):
    form = CourseForm(request.POST or None)

    if form.is_valid():
        # For adding the course
        course = Course()
        course.department = request.POST.get('department')
        course.course_name = request.POST.get('course_name')
        course.course_number = request.POST.get('course_number')
        course.credit_hours = request.POST.get('credit_hours')
        course.start_time = form.cleaned_data.get('start_time')
        course.end_time = form.cleaned_data.get('end_time')
        course.meeting_time_days = form.cleaned_data.get('meeting_time_days')
        course.instructor = CustomUser.objects.get(pk=request.user.pk)
        course.save()
        # For attaching the course to the user
        CustomUser.objects.get(pk=request.user.pk).courses.append(course)
        return redirect('course:courses')
    return render(request, 'course/courses-form.html', {'form': form})


def courses_delete(request, id):
    item = Course.objects.get(id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('course:courses')
    return render(request, 'course/courses-delete.html', {'item': item})


def courses_edit(request, id):
    item = Course.objects.get(id=id)
    form = CourseForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('course:courses')

    return render(request, 'course/courses-form.html', {'form': form, 'item': item})


def courses_enroll(request, id):
    CustomUser.objects.get(pk=request.user.pk).courses.append(Course.objects.get(id=id))
    print(f"users courses: {CustomUser.objects.get(pk=request.user.pk).courses}")
    return redirect('mysite:main')

