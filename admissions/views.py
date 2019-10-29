from django.shortcuts import render
from admissions.models import HighSchoolApplication
from register.models import Admin_Staff


def index(request, user_id):
    context = {"applications": get_applications(user_id)}
    return render(request, "admissions/index.html", context)


def detail(request, application_id):
    application = HighSchoolApplication.objects.get(id=application_id)
    context = {"application": application}
    return render(request, "admissions/detail.html", context)


def get_applications(user_id):
    admin_staff = Admin_Staff.objects.get(id=user_id)
    school_id = admin_staff.school_id
    return HighSchoolApplication.objects.filter(school_id=school_id)

