from django.urls import path
from django.conf.urls import include, url

from . import views

app_name = "changepass"
urlpatterns = [

    path("", views.index, name="index"),

]