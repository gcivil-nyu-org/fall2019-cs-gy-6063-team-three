from django.shortcuts import render
from OneApply.constants import UserType


def student(request):
    context = {
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "dashboard/student.html", context)


def admissionstaff(request):
    context = {
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "dashboard/admissionstaff.html", context)
