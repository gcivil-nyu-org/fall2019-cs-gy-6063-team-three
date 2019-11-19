from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import RecommendationForm
from register.models import Student
from OneApply.constants import UserType
from .models import Recommendation


def new_recommendation(request):
    # TODO Add test cases to check for unauthorized access
    if request.method == "POST":
        user_type = request.session.get("user_type", None)
        username = request.session.get("username", None)
        if (
            not request.session.get("is_login", None)
            or not username
            or user_type != UserType.STUDENT
        ):
            return redirect("landingpage:index")
        user = Student.objects.get(username=username)
        form = RecommendationForm(request.POST)
        context = {"form": form,
                   "recommendations": Recommendation.objects.filter(user_id=user.pk)
                   }
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = user.pk
            f.save()
            current_site = get_current_site(request)
            mail_subject = "Teacher Recommendation."
            message = render_to_string(
                "recommendation/sent_recommendation_email.html",
                {"user": f, "domain": current_site.domain},
            )
            to_email = form.cleaned_data["email_address"]
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            # TODO Add redirect button with response
            return HttpResponse(
                "An email has been sent to the teacher you added with instructions on how to fill out your recommendation!"  # noqa E501
            )
    else:
        form = RecommendationForm()
        context = {"form": form}
    return render(request, "recommendation/recommendation_form.html", context)


def all_recommendation(request):
    user_type = request.session.get("user_type", None)
    username = request.session.get("username", None)
    if (
        not request.session.get("is_login", None)
        or not username
        or user_type != UserType.STUDENT
    ):
        return redirect("landingpage:index")
    user = Student.objects.get(username=username)
    context = {"recommendations": Recommendation.objects.filter(user_id=user.pk)}
    return render(request, "recommendation/index.html", context)
