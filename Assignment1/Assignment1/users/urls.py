from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

app_name = 'users'

urlpatterns = [
    # /
    path('', views.login, name="home"),

    path('admin/', admin.site.urls),
    path('', include('mysite.urls')),
    path('calendar/', views.calendar, name="calendar"),
    path('courses/', views.courses, name="courses"),
    path('addcourses', views.courses_add, name="add_courses"),
    path('courses/delete/<int:id>', views.courses_delete, name="delete_courses"),
    path('courses/edit/<int:id>', views.courses_edit, name="edit_courses"),


]
