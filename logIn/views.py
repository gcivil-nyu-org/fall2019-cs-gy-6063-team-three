from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from register.models import Student, Admin_Staff


def login_user(request, user_type):
    login_error = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if user_type == "student":
                user = Student.objects.filter(username=username, password=password)
                if user:
                    return HttpResponse("Yay! We do remember you... (Student)")
                else:
                    login_error = True
            elif user_type == "admin_staff":
                user = Admin_Staff.objects.filter(username=username, password=password)
                if user:
                    return HttpResponse("Yay! We do remember you... (Admin Staff)")
                else:
                    login_error = True
    else:
        form = LoginForm()
    return render(
        request,
        "logIn/index.html",
        {"form": form, "user_type": user_type, "login_error": login_error},
    )
