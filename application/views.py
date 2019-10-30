from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import HighSchoolApplicationForm
from .models import HighSchoolApplication
from django.utils import timezone
from django.urls import reverse


def draft_application(request, user_id):
    if request.method == "POST":
        form = HighSchoolApplicationForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = user_id
            f.application_number = str(user_id) + str(f.school) + str(f.program)
            f.submitted_date = timezone.now()
            try:
                if "Submit" in request.POST.get("submit"):
                    f.is_draft = False
                else:
                    f.is_draft = True
            except:  # noqa: E722
                pass
            f.save()
            return HttpResponseRedirect(reverse("application:index", args=(user_id,)))
    else:
        form = HighSchoolApplicationForm()
    context = {"form": form, "user_id": user_id}
    return render(request, "application/application-form.html", context)


def draft_existing_application(request, user_id, application_id):
    if request.method == "POST":
        form = HighSchoolApplicationForm(request.POST)
        if form.is_valid():
            f = HighSchoolApplication.objects.get(pk=application_id)
            form = form.save(commit=False)
            f.first_name = form.first_name
            f.last_name = form.last_name
            f.school = form.school
            f.program = form.program
            f.application_number = str(user_id) + str(f.school) + str(f.program)
            f.email_address = form.email_address
            f.phoneNumber = form.phoneNumber
            f.address = form.address
            f.gender = form.gender
            f.date_of_birth = form.date_of_birth
            f.gpa = form.gpa
            f.parent_name = form.parent_name
            f.parent_phoneNumber = form.parent_phoneNumber
            f.submitted_date = timezone.now()
            try:
                if "Submit" in request.POST.get("submit"):
                    f.is_draft = False
                    print("iiffff")
                else:
                    f.is_draft = True
                    print("elseeeee")
            except:  # noqa: E722
                f.is_draft = True
            f.save()
            return HttpResponseRedirect(reverse("application:index", args=(user_id,)))
    else:
        form = HighSchoolApplicationForm()
    context = {"form": form, "application_id": application_id, "user_id": user_id}
    return render(request, "application/index.html", context)


def index(request, user_id):
    context = {
        "applications": HighSchoolApplication.objects.filter(user_id=user_id),
        "user_id": user_id,
    }
    return render(request, "application/index.html", context)


def detail(request, user_id, application_id):
    application = HighSchoolApplication.objects.get(pk=application_id)
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
        "applications": HighSchoolApplication.objects.filter(user_id=user_id),
        "selected_school": application,
        "form": form,
        "user_id": user_id,
    }
    return render(request, "application/index.html", context)
