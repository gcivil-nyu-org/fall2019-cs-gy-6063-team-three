from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse

from .forms import HighSchoolApplicationForm
from .models import HighSchoolApplication
from register.models import Student
from high_school.models import Program
from OneApply.constants import UserType


APPLICATION_COUNT = 10


def new_application(request):
    username = check_current_session(request)
    if not username:
        return redirect("landingpage:index")
    try:
        error_count_app = None
        user = Student.objects.get(username=username)
        if (
            HighSchoolApplication.objects.filter(user=user.pk, is_draft=False).count()
            == APPLICATION_COUNT
        ):
            error_count_app = (
                "You can only submit " + str(APPLICATION_COUNT) + " applications"
            )
            form = None
        elif request.method == "POST":
            form = HighSchoolApplicationForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.user = user
                f.application_number = generate_application_number(
                    user.pk, f.school.dbn, f.program.pk
                )
                if HighSchoolApplication.objects.filter(
                    application_number=f.application_number
                ):
                    raise ValueError("Duplicate school and program selected")
                f.submitted_date = timezone.now()
                if request.POST.get("submit") is not None:
                    f.is_draft = False
                else:
                    f.is_draft = True
                f.save()
                return HttpResponseRedirect(
                    reverse("dashboard:application:all_applications")
                )
        else:
            form = HighSchoolApplicationForm(
                initial={
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email_address": user.email_address,
                }
            )
        context = {"form": form, "error_count_app": error_count_app}
    except ValueError as e:
        context = {"form": form, "program_error": e}
    return render(request, "application/application-form.html", context)


def save_existing_application(request, application_id):
    username = check_current_session(request)
    if not username:
        return redirect("landingpage:index")
    if request.method == "POST":
        try:
            f = HighSchoolApplication.objects.get(pk=application_id)
        except Exception:
            context = {"invalid_url_app": "Application not found."}
            return render(request, "application/index.html", context)
        new_req = request.POST.copy()
        new_req["school"] = f.school.pk
        new_req["program"] = f.program.pk
        form = HighSchoolApplicationForm(new_req, disable=True)
        if form.is_valid():
            user = Student.objects.get(username=username)
            form = form.save(commit=False)
            f.first_name = form.first_name
            f.last_name = form.last_name
            f.school = form.school
            f.program = form.program
            f.application_number = generate_application_number(
                user.pk, f.school.dbn, f.program.pk
            )
            f.email_address = form.email_address
            f.phoneNumber = form.phoneNumber
            f.address = form.address
            f.gender = form.gender
            f.date_of_birth = form.date_of_birth
            f.gpa = form.gpa
            f.parent_name = form.parent_name
            f.parent_phoneNumber = form.parent_phoneNumber
            f.submitted_date = timezone.now()
            if request.POST.get("submit") is not None:
                f.is_draft = False
            else:
                f.is_draft = True
            f.save()
            return HttpResponseRedirect(
                reverse("dashboard:application:all_applications")
            )
    else:
        form = HighSchoolApplicationForm()
        f = None
    context = {"form": form, "application_id": application_id, "selected_app": f}
    return render(request, "application/index.html", context)


def all_applications(request):
    username = check_current_session(request)
    if not username:
        return redirect("landingpage:index")
    user = Student.objects.get(username=username)
    context = {
        "applications": HighSchoolApplication.objects.filter(user_id=user.pk).order_by(
            "-is_draft", "-submitted_date"
        )
    }
    return render(request, "application/index.html", context)


def detail(request, application_id):
    username = check_current_session(request)
    if not username:
        return redirect("landingpage:index")
    try:
        application = HighSchoolApplication.objects.get(pk=application_id)
    except Exception:
        context = {"invalid_url_app": "Application not found."}
        return render(request, "application/index.html", context)
    user = Student.objects.get(username=username)
    data = {
        "pk": application.pk,
        "application_number": application.application_number,
        "first_name": application.first_name,
        "last_name": application.last_name,
        "email_address": application.email_address,
        "phoneNumber": application.phoneNumber,
        "date_of_birth": application.date_of_birth,
        "gender": application.gender,
        "address": application.address,
        "gpa": application.gpa,
        "parent_name": application.parent_name,
        "parent_phoneNumber": application.parent_phoneNumber,
        "school": application.school,
        "program": application.program,
    }
    form = HighSchoolApplicationForm(
        initial={"program": application.program, "school": application.school},
        data=data,
        disable=True,
    )
    context = {
        "applications": HighSchoolApplication.objects.filter(user_id=user.pk),
        "selected_app": application,
        "form": form,
    }
    return render(request, "application/index.html", context)


def generate_application_number(user_id, school_id, program_id):
    return str(user_id) + str(school_id) + str(program_id)


def load_programs(request):
    school_id = request.GET.get("selected_school_id")
    if school_id:
        programs = Program.objects.filter(high_school_id=school_id)
    else:
        programs = None
    return render(request, "application/loadPrograms.html", {"programs": programs})


def check_current_session(request):
    user_type = request.session.get("user_type", None)
    username = request.session.get("username", None)
    if not request.session.get("is_login", None) or user_type != UserType.STUDENT:
        username = None
    return username
