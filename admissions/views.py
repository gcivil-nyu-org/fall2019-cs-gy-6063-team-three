from django.shortcuts import render, redirect
from django.views.generic import ListView
from django_filters.views import FilterView

from OneApply.constants import UserType
from admissions.advfilters import ApplicationFilter
from application.models import HighSchoolApplication
from high_school.models import Program
from register.models import Admin_Staff
from recommendation.models import Recommendation

ALL = "All"


class IndexView(ListView, FilterView):
    filterset_class = ApplicationFilter
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
        context["unauth"] = self.unauth if self.unauth else None
        context["programs"] = get_programs(all_applications)
        context["current_program"] = self.program if self.program else ALL
        context["school_name"] = self.school_name if self.school_name else None
        context["form"] = self.filterset.form if self.filterset else None
        return context

    def get_queryset(self):
        user_type = self.request.session.get("user_type", None)
        username = self.request.session.get("username", None)
        # These two variables keep track of the selected program id and the
        # corresponding program
        self.program_id = None
        self.program = None
        self.unauth = False
        if not username or user_type != UserType.ADMIN_STAFF:
            self.program_id = None
            self.user = None
            self.program = None
            self.unauth = True
            self.school_name = None
            self.filterset = None
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
            self.program_id = self.request.GET.get("program")
            self.program = None
        except KeyError:
            self.program_id = None
            self.program = None

        self.school_name = self.user.school.school_name

        if self.program_id:
            applications = applications.filter(program__id=self.program_id).order_by(
                "-submitted_date"
            )
        # Only if the program is set and also we have applications for it, it means that
        # a program will exist, hence,
        if self.program_id and applications:
            self.program = Program.objects.get(id=self.program_id)
        self.filterset = ApplicationFilter(self.request.GET, queryset=applications)
        return self.filterset.qs.distinct()


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
        context["unauth"] = True
        context["application"] = None
        context["recommendation"] = None
        return render(request, "admissions/detail.html", context)
    try:
        application = HighSchoolApplication.objects.get(id=application_id)
    except HighSchoolApplication.DoesNotExist:
        application = None
    if application:
        username = request.session.get("username", None)
        admin_user = Admin_Staff.objects.get(username=username)
        if application.school != admin_user.school:
            context["unauth"] = True
            context["application"] = None
            return render(request, "admissions/detail.html", context)
        try:
            recommendation = Recommendation.objects.filter(user=application.user)
        except Recommendation.DoesNotExist:
            recommendation = None
        context["recommendation"] = recommendation
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
        p_list.sort(key=lambda x: x.name)
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
