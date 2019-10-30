from django.urls import path
from django.conf.urls import include, url
from . import views

app_name = "dashboard"
urlpatterns = [
    url("ut_admin_staff/", include("admissions.urls")),
    path("<str:user_type>/", views.dashboard, name="dashboard"),
]
