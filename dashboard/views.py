from django.shortcuts import render
from OneApply.constants import UserType
from django.shortcuts import redirect


def dashboard(request):
    context = {
        "user_type": request.session.get("user_type", None),
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    if not request.session.get("is_login", None):
        return redirect("landingpage:index")

    user_type = request.session.get("user_type", None)
    if user_type == UserType.ADMIN_STAFF:
        return redirect("dashboard:admissions:index")
    else:
        # TODO: Redirect to the student dashboard
        return render(request, "dashboard/index.html", context)


def logout(request):
    request.session.flush()
    return redirect("landingpage:index")
