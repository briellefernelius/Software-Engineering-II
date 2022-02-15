from django.urls import path, include

from course import views

app_name = 'course'

urlpatterns = [
    path('', views.courses, name="courses"),
    path('<int:id>', views.course_page, name="course_page"),
    path('<int:id>/addassignment/', views.assigment_add, name="add_assignment"),
    path('addcourses/', views.courses_add, name="add_courses"),
    path('drop/<int:id>', views.course_drop, name="drop_courses"),
    path('courses/enroll/<int:id>', views.courses_enroll, name="enroll_courses"),
    path('courses/delete/<int:id>', views.courses_delete, name="delete_courses"),
    path('courses/edit/<int:id>', views.courses_edit, name="edit_courses"),
    path('assignment/delete/<int:id>', views.assignment_delete, name="delete_assignment"),
    path('assignment/edit/<int:id>', views.assignment_edit, name="edit_assignment"),
]