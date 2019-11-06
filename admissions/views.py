from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import ListView

from OneApply.constants import UserType
from application.models import HighSchoolApplication
from register.models import Admin_Staff


# TODO: Change this to list view
def index(request):
    # TODO: This user ID is hard coded to 1, needs to be changed after sessions are
    #  implemented

    if request.session["user_type"] != UserType.ADMIN_STAFF:
        raise PermissionDenied("You are not authorised to view this page")
    user_id = 1
    applications = get_applications(user_id)
    program_list = get_programs(applications)

    context = {
        "user_type": UserType.ADMIN_STAFF,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
        "applications": applications,
        "programs": program_list,
    }
    return render(request, "admissions/index.html", context)


class IndexView(ListView):
    model = HighSchoolApplication
    paginate_by = 10
    context_object_name = "applications"
    template_name = "admissions/index.html"

    def get_context_data(self, **kwargs):
        user_id = 1
        context = super().get_context_data(**kwargs)
        context["user_type"] = UserType.ADMIN_STAFF
        context["constant_ut_student"] = UserType.STUDENT
        context["constant_ut_adminStaff"] = UserType.ADMIN_STAFF
        all_applications = get_applications(user_id=user_id)
        context["programs"] = get_programs(all_applications)
        context["current_program"] = self.program if self.program else "All"
        return context

    def get_queryset(self):
        # if self.request.session["user_type"] != UserType.ADMIN_STAFF:
        #     raise PermissionDenied("You are not authorised to view this page")
        user_id = 1
        applications = get_applications(user_id=user_id).order_by("-submitted_date")
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
    return HighSchoolApplication.objects.filter(school_id=school_id, is_draft=False)


def get_programs(applications):
    program_set = set()
    for application in applications:
        program_set.add(application.program)
    program_set.add("All")
    return list(sorted(program_set))
