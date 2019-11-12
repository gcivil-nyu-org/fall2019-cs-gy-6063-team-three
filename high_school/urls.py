from django.urls import path
from . import views


app_name = "high_school"

urlpatterns = [
    path("all_schools/", views.HighSchoolListView.as_view(), name="index"),
    path("all_schools/save/", views.save_highschool_data, name="save"),
    path("all_schools/<str:dbn>/", views.HighSchoolListView.as_view(), name="overview"),
]
