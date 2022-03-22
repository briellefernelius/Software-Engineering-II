from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from mysite import views as mysite_views
app_name = 'users'

urlpatterns = [
    # /
    path('', mysite_views.first_login, name="home"),
    path('admin/', admin.site.urls),
    # path('', include('mysite.urls')),
    path('calendar/', views.calendar, name="calendar"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/<int:id>', views.profile_edit, name="edit_profile"),
    path('pieChart/', views.pieChart, name="pieChart"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
