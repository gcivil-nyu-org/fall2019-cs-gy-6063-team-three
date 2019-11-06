from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    # TODO: Change this to path, and don't use rul
    url("ut_admin_staff/", include("admissions.urls")),
    path("", include("high_school.urls"), name="all_schools"),
    # Todo: change this for applications integration
    # include <application_app_name>.urls, name="application"
    # leave the initial path empty (""), check login.urls for more
    # path("", include("logIn.urls"), name="testing"),
    path("", include("application.urls"), name="applications"),
    path("<str:user_type>/", views.dashboard, name="dashboard"),

]
app_name = "dashboard"
