from django.urls import path
from . import views


app_name = "high_schools"

urlpatterns = [
    # path('', views.HighSchoolDetailView.as_view(), name='index')
    path('', views.home, name='index')
]
