from django.urls import path
from django.conf.urls import url
from . import views

app_name = "recommendation"

urlpatterns = [
    path("add_teacher/", views.new_recommendation, name="new_recommendation"),
    url(
        r"^recommendation_rating/(?P<uidb64>[0-9A-Za-z_\-]+)/$",
        # noqa: E501
        views.recommendation_rating,
        name="recommendation_rating",
    ),
]
