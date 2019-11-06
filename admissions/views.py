from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView

from OneApply.constants import UserType
from application.models import HighSchoolApplication
from register.models import Admin_Staff


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
        context["current_program"] = self.program if self.program else "All"
        return context

    def get_queryset(self):
        user_type = self.request.session.get("user_type", None)
        if user_type != UserType.ADMIN_STAFF:
            self.program = None
            self.user_id = None
            return []
        username = self.request.session.get("username", None)
        if not username:
            self.program = None
            self.user_id = None
            return []
        self.user = None
        try:
            self.user = Admin_Staff.objects.get(username=username)
        except Admin_Staff.DoesNotExist:
            return []
        applications = get_applications(admin_staff=self.user).order_by("-submitted_date")
        try:
            self.program = self.request.GET.get("p")
        except KeyError:
            self.program = None
        if self.program:
            if self.program == "All":
                return applications
            applications = applications.filter(program=self.program).order_by(
                "-submitted_date"
            )

        return applications


def detail(request, application_id):
    if not request.session.get("is_login", None):
        return redirect("landingpage:index")
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


def get_applications(admin_staff):
    print(admin_staff)
    if not admin_staff:
        return []
    school_id = admin_staff.school_id
    return HighSchoolApplication.objects.filter(school_id=school_id, is_draft=False)


def get_programs(applications):
    program_set = set()
    for application in applications:
        program_set.add(application.program)
    program_set.add("All")
    return list(sorted(program_set))
