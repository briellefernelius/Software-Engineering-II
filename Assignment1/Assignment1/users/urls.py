from . import views
from django.urls import path
from django.conf.urls import url

app_name = 'users'

urlpatterns = [
    # /
    path('', views.login, name="home"),
]