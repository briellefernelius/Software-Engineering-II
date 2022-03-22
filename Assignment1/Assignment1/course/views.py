from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from course.forms import CourseForm, AssignmentForm, SubmissionForm, SubmissionForm_file, GradingForm
from users.models import CustomUser
from course.models import Course, CourseUser, Assignment, Submission
from mysite.views import Get_Messages, Message_Students_In_Course, Message_Student_Submitted

User = get_user_model()


def course_page(request, id):
    course = Course.objects.get(pk=id)
    assignments = Assignment.objects.all().filter(course=id)
    user = CustomUser.objects.get(pk=request.user.pk)
    submission = Submission.objects.all().filter(user=user)

    # Calculating the students grade
    all_points = 0
    earned_points = 0
    grade = ''
    max = assignments
    points_recieved = submission
    for points in max:
        points = points.max_points
        all_points += points
        print(f"all point {all_points}")

    for total_points in points_recieved:
        total_points = total_points.points_received
        if all_points != 0:
            earned_points += total_points
            print(f"earned {earned_points}")
            total = earned_points / all_points * 100
            print(f"2nd all {all_points}")
            print(f"total_points {total_points}")
            print(f"total {total}")

            if 94 <= total <= 100:
                grade = 'A'
            elif 90 <= total < 94:
                grade = 'A-'
            elif 87 <= total < 90:
                grade = 'B+'
            elif 84 <= total < 87:
                grade = 'B'
            elif 80 <= total < 84:
                grade = 'B-'
            elif 77 <= total < 80:
                grade = 'C+'
            elif 74 <= total < 77:
                grade = 'C'
            elif 70 <= total < 74:
                grade = 'C-'
            elif 67 <= total < 70:
                grade = 'D+'
            elif 64 <= total < 67:
                grade = 'D'
            elif 60 <= total < 64:
                grade = 'D-'
            else:
                grade = 'E'

    context = {
        'course': course,
        'assignments': assignments,
        'submission': submission,
        'grade': grade,
    }

    messages = Get_Messages(request)
    context.update(messages)

    return render(request, 'course/course_page.html', context)


def courses(request):
    item_list = Course.objects.all()
    context = {'item_list': item_list}
    messages = Get_Messages(request)
    context.update(messages)
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
        course = Course.objects.get(pk=id)
        assignments = Assignment.objects.all().filter(course=id)
        context = {
            'course': course, 'assignments': assignments
        }
        Message_Students_In_Course(request, id, assignment.id)

        messages = Get_Messages(request)
        context.update(messages)  # merging the context dictionary with the messages dictionary
        return render(request, 'course/course_page.html', context)
    return render(request, 'course/assignment-form.html', {'form': form, 'course': id})


def assignment_delete(request, courseid, assignmentid):
    assignments = Assignment.objects.get(id=assignmentid)

    if request.method == 'POST':
        assignments.delete()
        return redirect('course:course_page', courseid)
    return render(request, 'course/assignment-delete.html', {'assignments': assignments})


def assignment_edit(request, courseid, assignmentid):
    assignments = Assignment.objects.get(id=assignmentid)
    form = AssignmentForm(request.POST or None, instance=assignments)

    if form.is_valid():
        form.save()
        course = Course.objects.get(pk=courseid)
        assignments = Assignment.objects.all().filter(course=courseid)
        context = {'course': course, 'assignments': assignments}
        messages = Get_Messages(request)
        context.update(messages)  # merging the context dictionary with the messages dictionary

        return render(request, 'course/course_page.html', context)
    context = {'form': form, 'assignments': assignments, 'previous_page': request.META.get('HTTP_REFERER')}
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary
    return render(request, 'course/assignment-form.html', context)


def submit_assignment(request, course_id, assignment_id):

    user = CustomUser.objects.get(pk=request.user.pk)
    assignment = Assignment.objects.get(id=assignment_id)
    current_course = Course.objects.get(pk=course_id)
    submitted = False

    total = 0
    grade_list = []
    min_grade = assignment.max_points
    max_grade = 0
    avg = 0

    submission_list = Submission.objects.all().filter(assignment=assignment_id)
    for sub in submission_list:
        if sub.is_graded:
            grade_list.append(int(sub.points_received))
            if sub.points_received < min_grade:
                min_grade = sub.points_received
            if sub.points_received > max_grade:
                max_grade = sub.points_received
            total += sub.points_received
    print(f"grade list {grade_list}")

    print(f"Min = {min_grade}, Max = {max_grade}, Avg = {avg} ")

    def Average(list):
        if len(list) != 0:
            return sum(list) / len(list)

    if len(grade_list) != 0:
        avg = round(Average(grade_list))
    #print(f"Min = {min_grade}, Max = {max_grade}, Avg = {avg} ")

    # Check if already a submission
    try:
        submit = Submission.objects.get(user=user, assignment=assignment)
    except Submission.DoesNotExist:
        submit = None

    if submit is not None:
        #messages.warning(request, "Already submitted this assignment")
        submitted = True

    type = assignment.submission_type
    if type == '.file':
        form = SubmissionForm_file(request.POST or None, request.FILES or None)
    else:
        form = SubmissionForm(request.POST or None)

    ##### Unit test make sure student is submitting an assignment #####
    # Make sure already not submission #
    try:
        Submission.objects.get(user=user, assignment=assignment)
        print(f"Submission already exists, can't submit. Passed!")
    except Submission.DoesNotExist:
        print(f"If you can submit, Failed.")

    if form.is_valid():
        submission = form.save(commit=False)
        submission.user = CustomUser.objects.get(pk=request.user.pk)
        submission.assignment = Assignment.objects.get(pk=assignment_id)
        submission.max_points = assignment.max_points
        submission.save()

        return redirect('course:course_page', current_course.id)

    ##### UNIT Test continued ########
    # Make sure submission is added and for the correct assignment #
    try:
        submit_list = Submission.objects.all().filter(user=user, assignment=assignment)
        ## make sure only one added ##
        if len(submit_list) == 1:
            print(f"Submission added, 1 of 1.  Passed!")
    except Submission.DoesNotExist:
        print(f"Submission Does Not Exist.")

    context = {
        'form': form,
        'course': current_course,
        'assignment': assignment,
        'submitted': submitted,
        'submit': submit,
        'min': min_grade,
        'max': max_grade,
        'avg': avg
    }
    messages = Get_Messages(request)
    context.update(messages)
    return render(request, 'course/submit_assignment.html', context)


def assignment_submission(request, assignment_id):
    submission_list = Submission.objects.all().filter(assignment=assignment_id)
    course = Course.objects.get(assignment=assignment_id)
    context = {
        'list': submission_list,
        'course': course
    }
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary
    return render(request, 'course/assignment_submission.html', context)


def gradebook(request, submitid):
    submission = Submission.objects.get(pk=submitid)
    form = GradingForm(request.POST or None, instance=submission)
    assignment = submission.assignment

    context = {
        'form': form,
        'submission': submission,
        'assignment': assignment
    }
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary

    if form.is_valid():
        submission = form.save(commit=False)
        submission.is_graded = True
        submission.save()

        #Send message to students
        Message_Student_Submitted(request, submission.id)

        return redirect('course:assignment_submission', assignment.id)
    return render(request, 'course/gradebook.html', context)


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
        print(f"New Course created: {courseuser}") #For unit test

        ### Cookies ###
        cookie_courses = request.session.get('courses')
        cookie_courseuser = request.session.get('courseuser')
        # add new data to them
        cookie_courses.append(course.pk)
        cookie_courseuser.append(courseuser.pk)
        # save these cookies
        request.session['course'] = cookie_courses
        request.session['courseuser'] = cookie_courseuser
        ###############
        return redirect('course:courses')
    return render(request, 'course/courses-form.html', {'form': form})


def course_drop(request, id):
    # delete the course from the CourseUser database
    # then remove it from the users.courses list
    user = CustomUser.objects.get(pk=request.user.pk)
    courseuser = CourseUser.objects.all().filter(user_id=request.user.pk, course_id=id)

    for course in courseuser:
        #print(f"...Deleting course: {course} from user")
        course.delete()
    return redirect('mysite:main')


def courses_delete(request, id):
    item = Course.objects.get(id=id)

    if request.method == 'POST':
        item.delete()
        print(f"Deleting course: {item} from user") #For unit test

        return redirect('course:courses')
    return render(request, 'course/courses-delete.html', {'item': item})


def courses_edit(request, id):
    item = Course.objects.get(id=id)
    form = CourseForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('course:courses')
    context = {'form': form, 'item': item}
    messages = Get_Messages(request)
    context.update(messages)  # merging the context dictionary with the messages dictionary
    return render(request, 'course/courses-form.html', context)


# This function will either enroll or drop the course with the id that is passed in.
# If the user is already registered to that course, then it will be dropped.
def courses_enroll(request, id):
    # CustomUser.objects.get(pk=request.user.pk).courses.append(Course.objects.get(id=id))
    # since this function will be called by register and drop buttons
    # check to see if they are already registered to that course,
    # if they are, then drop that class
    # if they aren't, then add that class
    usercourses = CourseUser.objects.all().filter(user_id=request.user.pk)
    item_list = Course.objects.all()

    title_name = request.GET.get('title_name')
    department = request.GET.get('department')
    if title_name != '' and title_name is not None:
        item_list = item_list.filter(course_name__icontains=title_name)
    if department != '' and department is not None:
        item_list = item_list.filter(department__icontains=department)

    courseFound = False
    for course in usercourses:
        print(f'Course: {course.course_id}\n')
        if course.course_id.id == id:
            courseFound = True

    # Then add it to the user's courses
    if courseFound is False:
        courseuser = CourseUser()
        courseuser.course_id = Course.objects.get(pk=id)
        courseuser.user_id = CustomUser.objects.get(pk=request.user.pk)
        courseuser.save()
        print(f"New CourseUser created: {courseuser}")
    else:
        print("!!You are already registered to that course!!")
        course_drop(request, id)


    course_list = list()
    coursuser_list = list()
    temp = CourseUser.objects.all().filter(user_id=request.user.pk)
    for course in temp:
        course_list.append(course.course_id.pk)
        coursuser_list.append(course.pk)
    request.session['courses'] = course_list
    request.session['courseuser'] = coursuser_list
    # print(f'REGISTER cookie courses set: {course_list}')
    print(f'courses cookie data:\t', request.session['courses'])

    return redirect('mysite:registerClasses')