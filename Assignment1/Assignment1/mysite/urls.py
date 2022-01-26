from . import views
from django.urls import path

app_name = 'mysite'
urlpatterns = [
    path('', views.home, name="home"),
    path('main/', views.main, name="main"),
]