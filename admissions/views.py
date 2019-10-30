from django.shortcuts import render

from OneApply.constants import UserType
from admissions.models import HighSchoolApplication
from register.models import Admin_Staff


# TODO: Change this to list view
def index(request):
    # TODO: This user ID is hard coded to 1, needs to be changed after sessions are
    #  implemented
    user_id = 1
    applications = get_applications(user_id)
    context = {
        "user_type": UserType.ADMIN_STAFF,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
        "applications": applications,
    }
    return render(request, "admissions/index.html", context)


def detail(request, application_id):
    try:
        application = HighSchoolApplication.objects.get(id=application_id)
    except HighSchoolApplication.DoesNotExist:
        application = None
    context = {
        "user_type": UserType.ADMIN_STAFF,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
        "application": application,
    }
    return render(request, "admissions/detail.html", context)


def get_applications(user_id):
    try:
        admin_staff = Admin_Staff.objects.get(id=user_id)
    except Admin_Staff.DoesNotExist:
        return []
    school_id = admin_staff.school_id
    return HighSchoolApplication.objects.filter(school_id=school_id)
