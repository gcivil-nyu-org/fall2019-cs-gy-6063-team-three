from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.hashers import check_password

from OneApply.constants import UserType
from register.models import Student, Admin_Staff
from .forms import LoginForm


def login_user(request, user_type):
    verif_error = False
    valid_error = False
    login_error = False
    if request.session.get("is_login", None):
        return redirect("dashboard:dashboard")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if user_type == UserType.STUDENT:
                try:
                    user = Student.objects.get(username=username)
                except ObjectDoesNotExist:
                    login_error = True
                else:
                    if not user.is_active:
                        valid_error = True
                    elif not check_password(password, user.password):
                        login_error = True
                    else:
                        request.session["username"] = username
                        request.session["is_login"] = True
                        request.session["user_type"] = UserType.STUDENT
                        request.session["user_fname"] = user.first_name
                        return redirect("dashboard:dashboard")
            elif user_type == UserType.ADMIN_STAFF:
                try:
                    user = Admin_Staff.objects.get(username=username)
                except ObjectDoesNotExist:
                    login_error = True
                else:
                    if not user.is_verified_employee:
                        verif_error = True
                    elif not user.is_active:
                        valid_error = True
                    elif not check_password(password, user.password):
                        login_error = True
                    else:
                        request.session["username"] = username
                        request.session["is_login"] = True
                        request.session["user_type"] = UserType.ADMIN_STAFF
                        request.session["user_fname"] = user.first_name
                        return redirect("dashboard:dashboard")
    else:
        form = LoginForm()
    context = {
        "form": form,
        "user_type": user_type,
        "verif_error": verif_error,
        "login_error": login_error,
        "valid_error": valid_error,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "logIn/index.html", context)
