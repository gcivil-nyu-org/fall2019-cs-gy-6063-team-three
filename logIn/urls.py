from django.urls import path
from . import views

app_name = 'logIn'

urlpatterns = [
    # path('', views.login_user, name="login_user"),
    path('<int:user_type>/', views.login_user, name='login_user'),
]