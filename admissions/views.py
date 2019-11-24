from django.shortcuts import render, redirect
from django.views.generic import ListView

from OneApply.constants import UserType
from application.models import HighSchoolApplication
from high_school.models import Program
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
        # These two variables keep track of the selected program id and the
        # corresponding program
        self.program_id = None
        self.program = None
        if not username or user_type != UserType.ADMIN_STAFF:
            self.program_id = None
            self.user = None
            self.program = None
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
            # Get program id from request params
            self.program_id = self.request.GET.get("p")
            self.program = None
        except KeyError:
            self.program_id = None
            self.program = None

        if self.program_id:
            applications = applications.filter(program__id=self.program_id).order_by(
                "-submitted_date"
            )
        # Only if the program is set and also we have applications for it, it means that
        # a program will exist, hence,
        if self.program_id and applications:
            self.program = Program.objects.get(id=self.program_id)
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
    school = admin_staff.school
    return HighSchoolApplication.objects.filter(school=school, is_draft=False)


def get_programs(applications):
    p_list = []
    for application in applications:
        if application.program not in p_list:
            p_list.append(application.program)
    p_list = sorted(p_list)
    return p_list


def reject(request, application_id):
    application = HighSchoolApplication.objects.get(id=application_id)
    application.application_status = "0"
    application.save()
    return redirect("dashboard:admissions:index")


def accept(request, application_id):
    application = HighSchoolApplication.objects.get(id=application_id)
    application.application_status = "1"
    application.save()
    return redirect("dashboard:admissions:index")
