from django.shortcuts import render
from .forms import LoginForm
from register.models import Student, Admin_Staff
from OneApply.constants import UserType


def login_user(request, user_type):
    context = {
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    login_error = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if user_type == UserType.STUDENT:
                user = Student.objects.filter(username=username, password=password)
                if user:
                    return render(request, "dashboard/student.html", context)
                else:
                    login_error = True
            elif user_type == UserType.ADMIN_STAFF:
                user = Admin_Staff.objects.filter(username=username, password=password)
                if user:
                    return render(request, "dashboard/admissionstaff.html", context)
                else:
                    login_error = True
    else:
        form = LoginForm()
    context = {
        "form": form,
        "user_type": user_type,
        "login_error": login_error,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "logIn/index.html", context)
