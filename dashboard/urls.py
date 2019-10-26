from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [path("admissionstaff/", views.admissionstaff, name="admissionstaff"),
				path("student/", views.student, name = "student")]
