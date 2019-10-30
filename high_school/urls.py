from django.urls import path
from . import views


app_name = "high_school"

urlpatterns = [
    path(
        "<str:user_type>/all_schools/", views.HighSchoolListView.as_view(), name="index"
    ),
    path("<str:user_type>/all_schools/save/", views.save_highschool_data, name="save"),
    path(
        "<str:user_type>/all_schools/<str:dbn>/",
        views.HighSchoolListView.as_view(),
        name="overview",
    ),
]
