from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from course.forms import CourseForm, AssignmentForm

# Create your views here.
from users.models import CustomUser
from course.models import Course, CourseUser, Assignment

User = get_user_model()


def course_page(request, id):
    course = Course.objects.get(pk=id)
    assignments = Assignment.objects.all().filter(course=id)
    context = {
        'course': course, 'assignments': assignments
    }
    return render(request, 'course/course_page.html', context)


def courses(request):
    item_list = Course.objects.all()
    context = {
        'item_list': item_list,
    }
    return render(request, 'course/courses.html', context)


def assigment_add(request, id):

    form = AssignmentForm(request.POST)
    if form.is_valid():
        assignment = Assignment()
        assignment.title = form.cleaned_data.get('title')
        assignment.description = form.cleaned_data.get('description')
        assignment.due_date = form.cleaned_data.get('due_date')
        assignment.max_points = form.cleaned_data.get('max_points')
        assignment.submission_type = form.cleaned_data.get('submission_type')
        assignment.course = Course.objects.get(pk=id)

        assignment.save()
        return redirect('course:course_page', id)
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

        courseuser = CourseUser()
        courseuser.course_id = Course.objects.get(pk=course.pk)
        courseuser.user_id = CustomUser.objects.get(pk=request.user.pk)
        courseuser.save()
        print(f"New CourseUser created: {courseuser}")

        return redirect('course:courses')
    return render(request, 'course/courses-form.html', {'form': form})


def course_drop(request, id):
    # delete the course from the CourseUser database
    # then remove it from the users.courses list
    user = CustomUser.objects.get(pk=request.user.pk)
    courseuser = CourseUser.objects.all().filter(user_id=request.user.pk)
    courseuser.filter(course_id=id)
    print(f"-----CourseUser Objects: {courseuser}")
    for course in courseuser:
        course.delete()
        try:
            # try and remove the course from their course list
            user.courses.remove(course)
        except ValueError:
            # if the course is not already in their course list, then add it
            print("The course was not found in user.courses --Called From course/views.py:course_drop.")
    print(f"-----CourseUser Objects: {CourseUser.objects.all()}")
    return render(request, 'mysite/main.html')


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

    courseuser = CourseUser()
    courseuser.course_id = Course.objects.get(pk=id)
    courseuser.user_id = CustomUser.objects.get(pk=request.user.pk)
    courseuser.save()
    print(f"New CourseUser created: {courseuser}")

    #print(f"users courses: {CustomUser.objects.get(pk=request.user.pk).courses}")
    return redirect('mysite:main')

