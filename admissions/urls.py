from django.urls import path

from admissions.views import IndexView
from . import views

app_name = "admissions"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("detail/<int:application_id>", views.detail, name="detail"),
    path("accept/<int:application_id>", views.accept, name="accept"),
    path("reject/<int:application_id>", views.reject, name="reject"),
]
