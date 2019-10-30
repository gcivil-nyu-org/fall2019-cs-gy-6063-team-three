from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from register import views


urlpatterns = [
    path("", include("landingpage.urls", namespace="landingpage")),
    path("login/", include("logIn.urls")),
    path("register/", include("register.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("admin/", admin.site.urls),
    url(
        r"^activate_student_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",  # noqa: E501
        views.activate_student_account,
        name="activate_student_account",
    ),
    url(
        r"^verify_employee_status/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",  # noqa: E501
        views.verify_employee_status,
        name="verify_employee_status",
    ),
    url(
        r"^activate_admission_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",  # noqa: E501
        views.activate_admission_account,
        name="activate_admission_account",
    ),
]
