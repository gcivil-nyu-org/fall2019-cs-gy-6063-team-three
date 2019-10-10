from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    school = forms.CharField(label='Current School', max_length=100)
    borough = forms.CharField(label='Current Borough', max_length=20)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "school", "borough", "password1", "password2"]
