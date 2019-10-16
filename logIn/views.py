from django.shortcuts import render
from django.http import HttpResponse
from register.models import Student
from .forms import LoginForm


def login_user(request, user_type):
    login_error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user_type == "Student":
                user = Student.objects.filter(username=username, password=password)
                if user:
                    return HttpResponse("Yay! We do remember you...")
                else:
                    login_error = True                        
    else:
        form = LoginForm()
    return render(request, 'logIn/index.html', {'form': form, 'login_error': login_error})


