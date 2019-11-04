from django.urls import path
from . import views

app_name = "application"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<int:application_id>/", views.detail, name="overview"),
    path("apply/", views.new_application, name="draftApplication"),
    path(
        "detail/<int:application_id>/apply/",
        views.save_existing_application,
        name="draftExistingApplication",
    ),
]
