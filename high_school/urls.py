from django.urls import path
from . import views

app_name = "high_school"

urlpatterns = [
    path("all_schools/", views.HighSchoolListView.as_view(), name="index"),
    path("all_schools/save/", views.save_highschool_data, name="save"),
    path("all_schools/<str:dbn>/", views.HighSchoolListView.as_view(), name="overview"),
    path("all_schools/update_fav/<str:school_dbn>/<int:is_fav>",
         views.update_fav_hs,
         name="toggle_fav")
]
