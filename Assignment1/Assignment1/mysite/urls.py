from . import views
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

app_name = 'mysite'

urlpatterns = [
    # /
    path('', views.home, name="home"),

    # /main/
    path('main/', views.main, name="main"),
    # main/submission/
    re_path(r'^main/submission/$', views.submission_all, name="submission_all"),
    # main/submission/456/ = (site)/(submission_id)/
    re_path(r'^main/submission/(?P<submission_id>[0-9]+)/$', views.submission_with_id, name="submission_with_id"),

    re_path(r'^main/submission/(?P<submission_id>[0-9]+)/graded/$', views.submission_graded, name="submission_graded"),
    path('registerClasses/', views.register_classes, name="registerClasses"),
    path('createMessage/', views.create_message, name="create_message"),
    path('deleteMessage/<int:message_id>', views.delete_message, name="delete_message"),
    path('ignoreMessage/<int:message_id>', views.ignore_message, name="ignore_message"),
]

# INFO ON regular expressions
# ^ = startposition
# $ = endposition#
# () = group symbols
# ?P<> = save as a variable, for use when
# [0-9] = any number in range from 0 to 9, inclusive
# + = do as many times in expression
