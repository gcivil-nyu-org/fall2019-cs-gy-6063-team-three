from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import timedelta
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
        sub_date = timezone.now() - timedelta(days=180)
        objects = HighSchoolApplication.objects.filter(
            Q(user=user.pk, is_draft=False, submitted_date__gt=sub_date)
        )
        count = objects.count()
        error_apply = None
        form = None
        program_error = None
        confirmation_errors = None
        if count > 0:
            error_apply = "You can only submit all applications at once."
        elif count > APPLICATION_COUNT:
            error_count_app = (
                "You can only create " + str(APPLICATION_COUNT) + " applications"
            )
        elif request.method == "POST":
            count = 0
            form = HighSchoolApplicationForm(request.POST, user=user)
            school_list = []
            program_list = []
            for i in range(0, APPLICATION_COUNT):
                school = request.POST.get("school" + str(i))
                program = request.POST.get("program" + str(i))
                if school and program:
                    if school in school_list and program in program_list:
                        program_error = "Duplicate school and program selected"
                    school_list.append(school)
                    program_list.append(program)
                    count = count + 1
            if (
                request.POST.get("submit") is not None
                and request.POST.get("confirmation") is None
            ):
                confirmation_errors = "Confirm before submitting application"
            if not program_error and not confirmation_errors and form.is_valid():
                HighSchoolApplication.objects.filter(
                    Q(user=user.pk, is_draft=True, submitted_date__gt=sub_date)
                ).delete()
                f = form.save(commit=False)
                f.user = user
                f.submitted_date = timezone.now()
                if request.POST.get("submit") is not None:
                    f.is_draft = False
                else:
                    f.is_draft = True
                for i in range(0, count):
                    school = form.cleaned_data["school" + str(i)]
                    program = form.cleaned_data["program" + str(i)]
                    f.school = school
                    f.program = program
                    app_num = generate_application_number(
                        user.pk, school.dbn, program.pk
                    )
                    f.application_number = app_num
                    save_application(user, f)
                return HttpResponseRedirect(
                    reverse("dashboard:application:all_applications")
                )
        else:
            objects = HighSchoolApplication.objects.filter(
                Q(user=user.pk, is_draft=True, submitted_date__gt=sub_date)
            )
            count = objects.count()
            form = build_draft_form(user, objects)
        context = {
            "form": form,
            "error_count_app": error_count_app,
            "curr_schools": max(1, count),
            "error_apply": error_apply,
            "program_error": program_error,
            "confirmation_errors": confirmation_errors,
        }
    except ValueError as e:
        context = {"form": form, "program_error": e, "curr_schools": 0}
    return render(request, "application/application-form.html", context)


def save_existing_application(request, application_id):
    username = check_current_session(request)
    if not username:
        return redirect("landingpage:index")
    user = Student.objects.get(username=username)
    if request.method == "POST":
        try:
            f = HighSchoolApplication.objects.get(pk=application_id)
        except Exception:
            context = {"invalid_url_app": "Application not found."}
            return render(request, "application/index.html", context)
        new_req = request.POST.copy()
        new_req["school"] = f.school.pk
        new_req["program"] = f.program.pk
        form = HighSchoolApplicationForm(new_req, user=user)
        if form.is_valid():
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
        form = HighSchoolApplicationForm(user=user)
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
        user=user,
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


def build_draft_form(user, objects):
    if objects.count() != 0:
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
        initial = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email_address": user.email_address,
        }
    form = HighSchoolApplicationForm(
        initial=initial, max_count=APPLICATION_COUNT, user=user
    )
    return form


def save_application(user, form_object):
    return HighSchoolApplication.objects.create(
        first_name=form_object.first_name,
        last_name=form_object.last_name,
        user=user,
        school=form_object.school,
        program=form_object.program,
        application_number=form_object.application_number,
        email_address=form_object.email_address,
        phoneNumber=form_object.phoneNumber,
        address=form_object.address,
        gender=form_object.gender,
        date_of_birth=form_object.date_of_birth,
        gpa=form_object.gpa,
        parent_name=form_object.parent_name,
        parent_phoneNumber=form_object.parent_phoneNumber,
        submitted_date=timezone.now(),
        is_draft=form_object.is_draft,
    )
