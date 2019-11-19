from django.urls import path
from . import views

app_name = "recommendation"

urlpatterns = [
    path("add_teacher/", views.new_recommendation, name="new_recommendation"),
    path("recommended_teacher", views.all_recommendation, name="all_recommendation")
]
