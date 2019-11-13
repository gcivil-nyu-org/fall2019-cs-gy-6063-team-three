from django.urls import path
from django.conf.urls import include, url

from . import views

app_name = "dashboard"
urlpatterns = [
    # TODO: Change this to path, and don't use url
    url("ut_admin_staff/", include("admissions.urls")),
    path("", include("high_school.urls"), name="all_schools"),
    path("", views.dashboard, name="dashboard"),
    path("logout", views.logout, name="logout"),
    path("application/", include("application.urls"), name="application"),
    path("recommendation/", include("recommendation.urls"), name="recommendation"),
]
