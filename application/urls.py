from django.urls import path
from . import views

app_name = "application"

urlpatterns = [
    path("<int:user_id>/", views.index, name="index"),
    path("<int:user_id>/detail/<int:application_id>/", views.detail, name="overview"),
    path("<int:user_id>/apply/", views.draft_application, name="draftApplication"),
    path(
        "<int:user_id>/detail/<int:application_id>/apply/",
        views.draft_existing_application,
        name="draftExistingApplication",
    ),
]
