from django.urls import path

from . import views

app_name = "changepass"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "reset_password/<str:user_type>/", views.reset_password, name="reset_password"
    ),
]
