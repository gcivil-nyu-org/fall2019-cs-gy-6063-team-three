from django.urls import path
from . import views

app_name = "application"

urlpatterns = [
    path("all_applications/", views.all_applications, name="all_applications"),
    path(
        "all_applications/detail/<int:application_id>/", views.detail, name="overview"
    ),
    path("apply/", views.new_application, name="new_application"),
    path(
        "all_applications/detail/<int:application_id>/apply/",
        views.save_existing_application,
        name="draftExistingApplication",
    ),
    path("ajax/load-programs/", views.load_programs, name="ajax_load_programs"),
]
