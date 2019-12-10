from django.shortcuts import render
from OneApply.constants import UserType
from django.shortcuts import redirect
from .forms import changepassForm

def index(request):
    if not request.session.get("is_login", None):
        return redirect("landingpage:index")
    context = {
        "form": changepassForm(),
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "changepass/index.html",context)


def logout(request):
    request.session.flush()
    return redirect("landingpage:index")
# Create your views here.
