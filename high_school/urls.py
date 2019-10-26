from django.urls import path
from . import views


app_name = "high_school"

urlpatterns = [
    # path('', views.HighSchoolDetailView.as_view(), name='index')
    path('', views.HighSchoolListView.as_view(), name='index'),
    path('save/', views.save_highschool_data, name='save')
]
