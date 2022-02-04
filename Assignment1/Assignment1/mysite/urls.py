from . import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

app_name = 'mysite'

urlpatterns = [
    # /
    path('', views.home, name="home"),

    # /main/
    path('main/', views.main, name="main"),

    # main/courses/1/ = (site)/(course_id)
    #url(r'^(?P<course_id>[0-9]+)/$')

    # main/submission/
    url(r'^main/submission/$', views.submission_all, name="submission_all"),

    # main/submission/456/ = (site)/(submission_id)/
    url(r'^main/submission/(?P<submission_id>[0-9]+)/$', views.submission_with_id, name="submission_with_id"),

    url(r'^main/submission/(?P<submission_id>[0-9]+)/graded/$', views.submission_graded, name="submission_graded"),
]

# INFO ON regular expressions
# ^ = startposition
# $ = endposition#
# () = group symbols
# ?P<> = save as a variable, for use when
# [0-9] = any number in range from 0 to 9, inclusive
# + = do as many times in expression
