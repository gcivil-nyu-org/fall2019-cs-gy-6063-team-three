from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from register.models import User
from django.forms import ValidationError


def login_user(request):
    template_name = 'login/index.html'
    login_error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.filter(username=username, password=password)
            if user:
                return HttpResponse("Yay! We do remember you...")
            else:
                login_error = True
    else:
        form = LoginForm()
    return render(request,template_name,{'form': form, 'login_error': login_error})


