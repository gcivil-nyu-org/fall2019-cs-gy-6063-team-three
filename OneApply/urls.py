from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from register.views import (
    activate_student_account,
    verify_employee_status,
    activate_admission_account,
)
from recommendation.views import recommendation_rating

urlpatterns = [
    path("", include("landingpage.urls", namespace="landingpage")),
    path("login/", include("logIn.urls")),
    path("register/", include("register.urls")),
    path("admissions/", include("admissions.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("high_school/", include("high_school.urls")),
    path("recommendation/", include("recommendation.urls")),
    path("admin/", admin.site.urls),
    url(
        r"^activate_student_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",  # noqa: E501
        activate_student_account,
        name="activate_student_account",
    ),
    url(
        r"^verify_employee_status/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",  # noqa: E501
        verify_employee_status,
        name="verify_employee_status",
    ),
    url(
        r"^activate_admission_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",  # noqa: E501
        activate_admission_account,
        name="activate_admission_account",
    ),
    url(
        r"^recommendation_rating/(?P<uid1>[0-9A-Za-z_\-]+)/(?P<uid2>[0-9A-Za-z_\-]+)/$",  # noqa: E501
        recommendation_rating,
        name="recommendation_rating",
    ),
]
