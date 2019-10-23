from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from register import views


urlpatterns = [
    path("", include("landingpage.urls")),
    path("login/", include("logIn.urls")),
    path("register/", include("register.urls")),
    path("admin/", admin.site.urls),
    url(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",  # noqa: E501
        views.activate,
        name="activate",
    ),
]
