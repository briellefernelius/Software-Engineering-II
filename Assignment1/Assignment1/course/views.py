from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from course.forms import CourseForm, AssignmentForm, SubmissionForm
# Create your views here.
from users.models import CustomUser
from course.models import Course, CourseUser, Assignment, Submission

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


def assignment_delete(request, courseid, assignmentid):
    assignments = Assignment.objects.get(id=assignmentid)

    if request.method == 'POST':
        assignments.delete()
        return course_page(request, courseid)
    return render(request, 'course/assignment-delete.html', {'assignments': assignments})


def assignment_edit(request, courseid, assignmentid):
    assignments = Assignment.objects.get(id=assignmentid)
    form = AssignmentForm(request.POST or None, instance=assignments)

    if form.is_valid():
        form.save()
        return course_page(request, courseid)

    return render(request, 'course/assignment-form.html', {'form': form, 'assignments': assignments})


def submit_assignment(request, course_id, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    form = SubmissionForm(request.POST or None)
    current_course = Course.objects.get(pk=course_id)

    if form.is_valid():
        submission = Submission()
        submission.user = CustomUser.objects.get(pk=request.user.pk)
        submission.assignment = Assignment.objects.get(pk=assignment_id)
        submission.textbox = form.cleaned_data.get('textbox')
        submission.save()
        return redirect('course:course_page', course_id)

    return render(request, 'course/submit_assignment.html', {'form': form, 'course': current_course, 'assignment': assignment})


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
        course.start_date = form.cleaned_data.get('start_date')
        course.end_date = form.cleaned_data.get('end_date')
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
    courseuser = CourseUser.objects.all().filter(user_id=request.user.pk, course_id=id)

    print(f"-----CourseUser Objects: {courseuser}")
    for course in courseuser:
        print(f"...Deleting course: {course} from user")
        course.delete()
    return redirect('mysite:main')


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

    # since this function will be called by register and drop buttons
    # check to see if they are already registered to that course,
    # if they are, then drop that class
    # if they aren't, then add that class

    usercourses = CourseUser.objects.all().filter(user_id=request.user.pk)
    courseFound = False

    for course in usercourses.course_id:
        if course.id == id:
            courseFound = True

    # Then add it to the user's courses
    if courseFound is not True:
        courseuser = CourseUser()
        courseuser.course_id = Course.objects.get(pk=id)
        courseuser.user_id = CustomUser.objects.get(pk=request.user.pk)
        courseuser.save()
        print(f"New CourseUser created: {courseuser}")

    #print(f"users courses: {CustomUser.objects.get(pk=request.user.pk).courses}")
    return render(request, 'mysite/registerClasses.html', {'users_courses': usercourses})

