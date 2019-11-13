from django.urls import path
from . import views

app_name = "recommendation"

urlpatterns = [
    path("add_teacher/", views.new_recommendation, name="new_recommendation")
]
