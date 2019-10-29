from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from OneApply.constants import UserType
from register.models import Student, Admin_Staff
from .forms import LoginForm


def login_user(request, user_type):
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
                        return HttpResponse("Yay! We do remember you... (Student)")
            elif user_type == UserType.ADMIN_STAFF:
                user = Admin_Staff.objects.filter(username=username, password=password)
                if user:
                    return HttpResponseRedirect(reverse("admissions:index"),
                                                args=(user.id,))
                else:
                    login_error = True
    else:
        form = LoginForm()
    context = {
        "form": form,
        "user_type": user_type,
        "login_error": login_error,
        "valid_error": valid_error,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "logIn/index.html", context)
