from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from course import views

app_name = 'course'

urlpatterns = [
    path('', views.courses, name="courses"),
    path('<int:id>', views.course_page, name="course_page"),
    path('<int:id>/addassignment/', views.assigment_add, name="add_assignment"),
    path('<int:course_id>/<int:assignment_id>/submitassignment', views.submit_assignment, name="submit_assignment"),
    path('<int:assignment_id>/submissions', views.assignment_submission, name="assignment_submission"),
    path('addcourses/', views.courses_add, name="add_courses"),
    path('drop/<int:id>', views.course_drop, name="drop_courses"),
    path('courses/enroll/<int:id>', views.courses_enroll, name="enroll_coursews"),
    path('courses/delete/<int:id>', views.courses_delete, name="delete_courses"),
    path('courses/edit/<int:id>', views.courses_edit, name="edit_courses"),
    path('<int:courseid>/<int:assignmentid>/assignment/delete', views.assignment_delete, name="delete_assignment"),
    path('<int:courseid>/<int:assignmentid>/assignment/edit', views.assignment_edit, name="edit_assignment"),
    path('<int:submitid>/gradebook', views.gradebook, name="gradebook"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
