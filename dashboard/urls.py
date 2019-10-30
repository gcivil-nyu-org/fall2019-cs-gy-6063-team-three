from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [path("<str:user_type>/<int:user_id>", views.dashboard, name="dashboard")]
