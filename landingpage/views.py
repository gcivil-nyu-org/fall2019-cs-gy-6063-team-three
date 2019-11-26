from django.shortcuts import render, redirect
from OneApply.constants import UserType


# Create your views here.


def index(request):
    if request.session.get("is_login", None):
        return redirect("dashboard:dashboard")
    context = {
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "landingpage/index.html", context)
