from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

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
        objects = HighSchoolApplication.objects.filter(user=user.pk)
        if HighSchoolApplication.objects.filter(user=user.pk, is_draft=False):
            error_apply = "You can only submit all applications at once."
        else:
            error_apply = None
        count = objects.count()
        if count > APPLICATION_COUNT:
            error_count_app = (
                "You can only create " + str(APPLICATION_COUNT) + " applications"
            )
            form = None
        elif request.method == "POST":
            form = HighSchoolApplicationForm(request.POST)
            HighSchoolApplication.objects.filter(user=user.pk, is_draft=True).delete()
            for i in range(0, APPLICATION_COUNT):
                new_req = request.POST.copy()
                new_req["school"] = request.POST.get("school" + str(i))
                new_req["program"] = request.POST.get("program" + str(i))
                if not new_req["school"] or not new_req["program"]:
                    continue
                form = HighSchoolApplicationForm(new_req)
                if form.is_valid():
                    f = form.save(commit=False)
                    app_num = generate_application_number(
                        user.pk, f.school.dbn, f.program.pk
                    )
                    f.application_number = app_num
                    f.user = user
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
            if count != 0:
                initial = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email_address": user.email_address,
                    "phoneNumber": objects[0].phoneNumber,
                    "address": objects[0].address,
                    "gender": objects[0].gender,
                    "date_of_birth": objects[0].date_of_birth.strftime("%Y-%m-%d"),
                    "gpa": objects[0].gpa,
                    "parent_name": objects[0].parent_name,
                    "parent_phoneNumber": objects[0].parent_phoneNumber,
                }
                i = 0
                for obj in objects:
                    if obj.is_draft:
                        initial["school" + str(i)] = obj.school.pk
                        initial["program" + str(i)] = obj.program.pk
                        i = i + 1
                    else:
                        count = count - 1
            else:
                initial = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email_address": user.email_address,
                }
            form = HighSchoolApplicationForm(
                initial=initial, max_count=APPLICATION_COUNT
            )
        context = {
            "form": form,
            "error_count_app": error_count_app,
            "curr_schools": max(1, count),
            "error_apply": error_apply,
        }
    except ValueError as e:
        context = {"form": form, "program_error": e, "curr_schools": 0}
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
        form = HighSchoolApplicationForm(new_req)
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
        "applications": HighSchoolApplication.objects.filter(
            user_id=user.pk, is_draft=False
        ).order_by("-submitted_date")
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
    )
    context = {
        "applications": HighSchoolApplication.objects.filter(user_id=user.pk),
        "selected_app": application,
        "form": form,
    }
    return render(request, "application/index.html", context)


def withdraw_application(request, application_id):
    username = check_current_session(request)
    if not username:
        return redirect("landingpage:index")
    try:
        application = HighSchoolApplication.objects.get(pk=application_id)
    except Exception:
        context = {"invalid_url_app": "Application not found."}
        return render(request, "application/index.html", context)
    application.application_status = 3
    application.save()
    return HttpResponseRedirect(reverse("dashboard:application:all_applications"))


def generate_application_number(user_id, school_id, program_id):
    return str(user_id) + str(school_id) + str(program_id)


@csrf_exempt
def load_programs(request):
    try:
        school_id = request.POST.get("selected_school_id")
        programs = None
        prog = json.loads(request.POST.get("prog", None))
        if school_id:
            programs = Program.objects.filter(high_school_id=school_id)
            if programs.count() == 0:
                p = Program(
                    high_school_id=school_id, name="General program", code=school_id
                )
                try:
                    p.save()
                    programs = Program.objects.filter(high_school_id=school_id)
                except Exception:
                    programs = None
            elif prog:
                programs = programs.exclude(pk__in=prog)
    except Exception:
        programs = None
    return render(request, "application/loadPrograms.html", {"programs": programs})


def check_current_session(request):
    user_type = request.session.get("user_type", None)
    username = request.session.get("username", None)
    if not request.session.get("is_login", None) or user_type != UserType.STUDENT:
        username = None
    return username
