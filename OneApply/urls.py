from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include("landingpage.urls", namespace="ladndingpage")),
    path("login/", include("logIn.urls")),
    path("register/", include("register.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("admin/", admin.site.urls),
]
