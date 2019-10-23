from django.shortcuts import render
from django.http import HttpResponse
from register.models import Student
from .forms import LoginForm


def login_user(request, user_type):
    valid_error = False
    login_error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user_type == "Student":
                user = Student.objects.get(username=username)
                if not user.is_active:
                    valid_error = True
                elif user.password != password:
                    login_error = True
                else:
                    return HttpResponse("Yay! We do remember you...")
    else:
        form = LoginForm()
    return render(request, 'logIn/index.html', {'form': form, 'login_error': login_error, 'valid_error': valid_error})


