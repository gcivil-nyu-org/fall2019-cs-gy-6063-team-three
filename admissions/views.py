from django.shortcuts import render
from admissions.models import Application


def index(request):
    context = {
        "applications": Application.objects.all(),
    }
    return render(request, "admissions/index.html", context)


def detail(request, application_id):
    application = Application.objects.get(application_id=application_id)
    print(application)
    context = {
        "application": application,
    }
    return render(request, "admissions/detail.html", context)
