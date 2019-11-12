from django.urls import path
from . import views

app_name = "recommendation"

urlpatterns = [
    path("<str:user_type>/all_recommendations", views.all_recommendation, name="all_recommendation"),
]
