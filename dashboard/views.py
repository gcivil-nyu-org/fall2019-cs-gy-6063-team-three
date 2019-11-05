from django.shortcuts import render
from OneApply.constants import UserType
from django.shortcuts import redirect


def dashboard(request, user_type):
    context = {
        "user_type": user_type,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    if not request.session.get("is_login", None):
        return redirect("landingpage:index")
    return render(request, "dashboard/index.html", context)


def logout(request):
    request.session.flush()
    return redirect("landingpage:index")
