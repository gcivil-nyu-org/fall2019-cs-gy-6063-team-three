from django.shortcuts import render
from OneApply.constants import UserType


def dashboard(request, user_type, user_id):
    context = {
        "user_type": user_type,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
        "user_id": user_id,
    }
    return render(request, "dashboard/index.html", context)
