from django.urls import path
from django.conf.urls import include, url

from . import views

app_name = "dashboard"
urlpatterns = [
    # TODO: Change this to path, and don't use rul
    url("ut_admin_staff/", include("admissions.urls")),
    path("", include("high_school.urls"), name="all_schools"),
    # Todo: change this for applications integration
    # include <application_app_name>.urls, name="application"
    # leave the initial path empty (""), check login.urls for more
    # path("", include("logIn.urls"), name="testing"),
    path("", views.dashboard, name="dashboard"),
    path("logout", views.logout, name="logout"),
    path("", include("application.urls"), name="application"),
]
