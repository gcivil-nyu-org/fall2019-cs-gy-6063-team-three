from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse

from .forms import HighSchoolApplicationForm
from .models import HighSchoolApplication
from register.models import Student
from high_school.models import Program
from OneApply.constants import UserType


def new_application(request):
    user_type = request.session.get("user_type", None)
    username = request.session.get("username", None)
    if (
        not request.session.get("is_login", None)
        or not username
        or user_type != UserType.STUDENT
    ):
        return redirect("landingpage:index")
    try:
        if request.method == "POST":
            user = Student.objects.get(username=username)
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
            form = HighSchoolApplicationForm()
        context = {"form": form}
    except ValueError as e:
        context = {"form": form, "program_error": e}
    return render(request, "application/application-form.html", context)


def save_existing_application(request, application_id):
    user_type = request.session.get("user_type", None)
    username = request.session.get("username", None)
    if (
        not request.session.get("is_login", None)
        or not username
        or user_type != UserType.STUDENT
    ):
        return redirect("landingpage:index")
    if request.method == "POST":
        form = HighSchoolApplicationForm(request.POST)
        if form.is_valid():
            user = Student.objects.get(username=username)
            f = HighSchoolApplication.objects.get(pk=application_id)
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
    context = {"form": form, "application_id": application_id}
    return render(request, "application/index.html", context)


def all_applications(request):
    user_type = request.session.get("user_type", None)
    username = request.session.get("username", None)
    if (
        not request.session.get("is_login", None)
        or not username
        or user_type != UserType.STUDENT
    ):
        return redirect("landingpage:index")
    user = Student.objects.get(username=username)
    context = {"applications": HighSchoolApplication.objects.filter(user_id=user.pk)}
    return render(request, "application/index.html", context)


def detail(request, application_id):
    user_type = request.session.get("user_type", None)
    username = request.session.get("username", None)
    if (
        not request.session.get("is_login", None)
        or not username
        or user_type != UserType.STUDENT
    ):
        return redirect("landingpage:index")
    application = HighSchoolApplication.objects.get(pk=application_id)
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
    form = HighSchoolApplicationForm(data)
    context = {
        "applications": HighSchoolApplication.objects.filter(user_id=user.pk),
        "selected_app": application,
        "form": form,
    }
    # TODO redirect to index
    return render(request, "application/application-overview.html", context)


def generate_application_number(user_id, school_id, program_id):
    return str(user_id) + str(school_id) + str(program_id)


def load_programs(request):
    school_id = request.GET.get("selected_school_id")
    if school_id:
        programs = Program.objects.filter(high_school_id=school_id)
    else:
        programs = None
    return render(request, "application/loadPrograms.html", {"programs": programs})
