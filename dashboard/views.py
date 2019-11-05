from django.shortcuts import render
from OneApply.constants import UserType


def dashboard(request, user_type):
    context = {
        "user_type": user_type,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "dashboard/index.html", context)
