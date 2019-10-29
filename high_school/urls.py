from django.urls import path
from . import views


app_name = "high_school"

urlpatterns = [
    path("", views.HighSchoolListView.as_view(), name="index"),
    path("save/", views.save_highschool_data, name="save"),
    path("<str:dbn>/", views.HighSchoolListView.as_view(), name="overview"),
]
