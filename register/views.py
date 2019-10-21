from django.http import HttpResponse
from django.shortcuts import render
from .forms import StudentRegisterForm, AdminStaffRegisterForm
from OneApply.constants import UserType


def register_user(request, user_type):
    form = None
    if request.method == "POST":
        if user_type == UserType.STUDENT:
            form = StudentRegisterForm(request.POST)
        elif user_type == UserType.ADMIN_STAFF:
            form = AdminStaffRegisterForm(request.POST)
        if form is not None and form.is_valid():
            password = form.cleaned_data["input_password"]
            f = form.save(commit=False)
            f.password = password
            f.save()
            return HttpResponse("Registered Successfully!")
    else:
        if user_type == UserType.STUDENT:
            form = StudentRegisterForm()
        elif user_type == UserType.ADMIN_STAFF:
            form = AdminStaffRegisterForm()
    context = {
        "form": form,
        "user_type": user_type,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "register/index.html", context)
