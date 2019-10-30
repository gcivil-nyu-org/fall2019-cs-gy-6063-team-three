from django.urls import path
from . import views

app_name = "admissions"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<int:application_id>", views.detail, name="detail"),
]
