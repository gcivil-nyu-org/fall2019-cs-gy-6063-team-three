from OneApply.constants import UserType
from django.shortcuts import redirect


def dashboard(request):
    if not request.session.get("is_login", None):
        return redirect("landingpage:index")

    user_type = request.session.get("user_type", None)
    if user_type == UserType.ADMIN_STAFF:
        return redirect("dashboard:admissions:index")
    else:
        return redirect("dashboard:high_school:index")


def logout(request):
    request.session.flush()
    return redirect("landingpage:index")
