from django.conf.urls import include
from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", include("high_school.urls"), name="all_schools"),
    path("<str:user_type>/", views.dashboard, name="dashboard"),
]
