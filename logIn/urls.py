from django.urls import path
from . import views

app_name = "logIn"

urlpatterns = [path("<str:user_type>/", views.login_user, name="login_user")]
