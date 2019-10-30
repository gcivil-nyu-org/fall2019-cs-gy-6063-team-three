from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .forms import LoginForm
from register.models import Student, Admin_Staff
from OneApply.constants import UserType
from django.shortcuts import redirect


def login_user(request, user_type):
    verif_error = False
    valid_error = False
    login_error = False
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
                    elif user.password != password:
                        login_error = True
                    else:
                        return redirect("dashboard:dashboard", UserType.STUDENT)
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
                    elif user.password != password:
                        login_error = True
                    else:
                        return redirect("dashboard:dashboard", UserType.ADMIN_STAFF)
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
