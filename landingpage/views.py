from django.shortcuts import render
from OneApply.constants import UserType


# Create your views here.
def index(request):
    context = {
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "landingpage/index.html", context)
