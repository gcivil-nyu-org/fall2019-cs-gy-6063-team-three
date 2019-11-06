from django.shortcuts import render, redirect
from django.views.generic import ListView

from OneApply.constants import UserType
from application.models import HighSchoolApplication
from register.models import Admin_Staff

ALL = "All"


class IndexView(ListView):
    model = HighSchoolApplication
    paginate_by = 10
    context_object_name = "applications"
    template_name = "admissions/index.html"

    def get(self, *args, **kwargs):
        if not self.request.session.get("is_login", None):
            return redirect("landingpage:index")
        return super(IndexView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_type"] = UserType.ADMIN_STAFF
        context["constant_ut_student"] = UserType.STUDENT
        context["constant_ut_adminStaff"] = UserType.ADMIN_STAFF
        all_applications = get_applications(self.user)
        context["programs"] = get_programs(all_applications)
        context["current_program"] = self.program if self.program else ALL
        return context

    def get_queryset(self):
        user_type = self.request.session.get("user_type", None)
        username = self.request.session.get("username", None)
        if not username or user_type != UserType.ADMIN_STAFF:
            self.program = None
            self.user = None
            return []
        self.user = None
        try:
            self.user = Admin_Staff.objects.get(username=username)
        except Admin_Staff.DoesNotExist:
            return []
        applications = get_applications(admin_staff=self.user).order_by(
            "-submitted_date"
        )
        try:
            self.program = self.request.GET.get("p")
        except KeyError:
            self.program = None
        if self.program:
            if self.program == ALL:
                return applications
            applications = applications.filter(program=self.program).order_by(
                "-submitted_date"
            )
        return applications


def detail(request, application_id):
    if not request.session.get("is_login", None):
        return redirect("landingpage:index")
    user_type = request.session.get("user_type", None)
    context = {
        "user_type": UserType.ADMIN_STAFF,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
        "application": None,
    }
    if user_type != UserType.ADMIN_STAFF:
        context["user_type"] = UserType.STUDENT
        return render(request, "admissions/detail.html", context)
    try:
        application = HighSchoolApplication.objects.get(id=application_id)
    except HighSchoolApplication.DoesNotExist:
        application = None
    context["application"] = application
    return render(request, "admissions/detail.html", context)


def get_applications(admin_staff):
    if not admin_staff:
        return []
    school_id = admin_staff.school_id
    return HighSchoolApplication.objects.filter(school_id=school_id, is_draft=False)


def get_programs(applications):
    program_set = set()
    for application in applications:
        program_set.add(application.program)
    program_set.add(ALL)
    return list(sorted(program_set))
