from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import timezone
from .forms import RecommendationForm, RecommendationRatingForm
from register.models import Student
from OneApply.constants import UserType
from .models import Recommendation


def new_recommendation(request):
    user_type = request.session.get("user_type", None)
    username = request.session.get("username", None)
    if (
        not request.session.get("is_login", None)
        or not username
        or user_type != UserType.STUDENT
    ):
        return redirect("landingpage:index")
    if request.method == "POST":
        user = Student.objects.get(username=username)
        form = RecommendationForm(request.POST)
        form.user_id = user.pk
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = user.pk
            f.save()
            current_site = get_current_site(request)
            mail_subject = "Teacher Recommendation."
            message = render_to_string(
                "recommendation/sent_recommendation_email.html",
                {"user": f, "domain": current_site.domain, "uid1": f.pk},
            )
            to_email = form.cleaned_data["email_address"]
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.info(
                request,
                "An email has been sent to the teacher you added with instructions on how to fill out your recommendation!",  # noqa: E501
            )
            return redirect("dashboard:recommendation:new_recommendation")
    else:
        form = RecommendationForm()
    context = {"form": form}
    return render(request, "recommendation/recommendation_form.html", context)


"""
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
"""


def recommendation_rating(request, uid1):
    teacherRecommendation = Recommendation
    try:
        teacherRecommendation = Recommendation.objects.get(pk=uid1)
    except (TypeError, ValueError, OverflowError, teacherRecommendation.DoesNotExist):
        context = {"empty_list": 1}
        return render(request, "recommendation/recommendation_rating.html", context)
    if not teacherRecommendation.submitted_date:
        if request.method == "POST":
            form = RecommendationRatingForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                teacherRecommendation.known_length = f.known_length
                teacherRecommendation.known_strength = f.known_strength
                teacherRecommendation.known_location = f.known_location
                teacherRecommendation.rating_concepts = f.rating_concepts
                teacherRecommendation.rating_creativity = f.rating_creativity
                teacherRecommendation.rating_mathematical = f.rating_mathematical
                teacherRecommendation.rating_written = f.rating_written
                teacherRecommendation.rating_oral = f.rating_oral
                teacherRecommendation.rating_goals = f.rating_goals
                teacherRecommendation.rating_socialization = f.rating_socialization
                teacherRecommendation.rating_analyzing = f.rating_analyzing
                teacherRecommendation.rating_comment = f.rating_comment
                teacherRecommendation.submitted_date = timezone.now()
                teacherRecommendation.save()
                context = {"submitted": 1}
                return render(
                    request, "recommendation/recommendation_rating.html", context
                )
        else:
            form = RecommendationRatingForm()
        context = {"form": form, "teacher_recommendation": teacherRecommendation}
        return render(request, "recommendation/recommendation_rating.html", context)
    else:
        context = {"completed": 1}
        return render(request, "recommendation/recommendation_rating.html", context)
