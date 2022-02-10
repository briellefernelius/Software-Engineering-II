from django.urls import path, include

from course import views

app_name = 'course'

urlpatterns = [
    path('courses/', views.courses, name="courses"),
    path('<int:id>', views.course_page, name="course_page"),
    path('addcourses/', views.courses_add, name="add_courses"),
    path('courses/enroll/<int:id>', views.courses_enroll, name="courses_enroll"),
    path('courses/delete/<int:id>', views.courses_delete, name="delete_courses"),
    path('courses/edit/<int:id>', views.courses_edit, name="edit_courses"),
]