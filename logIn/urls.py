from django.urls import path
from . import views

app_name = "logIn"

urlpatterns = [path("<str:user_type>/login_user", views.login_user, name="login_user")]
# Todo: remove this comment post successful integration of application ap
# prefer to use the same pattern - '<str:user_type>/applications'
