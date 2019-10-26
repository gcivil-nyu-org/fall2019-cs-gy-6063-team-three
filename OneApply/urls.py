from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include("landingpage.urls")),
    path("login/", include("logIn.urls")),
    path("register/", include("register.urls")),
    path("high_schools/", include("high_schools.urls")),
    path("admin/", admin.site.urls),
]
