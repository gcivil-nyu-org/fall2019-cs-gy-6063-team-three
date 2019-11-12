from django.urls import path
from . import views

app_name = "application"

urlpatterns = [
    path(
        "<str:user_type>/all_applications/",
        views.all_applications,
        name="all_applications",
    ),
    path("<str:user_type>/detail/<int:application_id>/", views.detail, name="overview"),
    path("<str:user_type>/apply/", views.new_application, name="new_application"),
    path(
        "<str:user_type>/detail/<int:application_id>/apply/",
        views.save_existing_application,
        name="draftExistingApplication",
    ),
    path("ajax/load-programs/", views.load_programs, name="ajax_load_programs"),
]
