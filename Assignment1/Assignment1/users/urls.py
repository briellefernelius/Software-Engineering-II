from . import views
#from django.conf.urls import url
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
    path('profile/', views.profile, name="profile"),
    path('profile/edit/<int:id>', views.profile_edit, name="edit_profile"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
