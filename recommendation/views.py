from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import RecommendationForm, RecommendationRatingForm
from register.models import Student
from OneApply.constants import UserType
from .models import Recommendation

RECOMMENDATION_COUNT = 2


def new_recommendation(request):
    user_type = request.session.get("user_type", None)
    username = request.session.get("username", None)
    if (
        not request.session.get("is_login", None)
        or not username
        or user_type != UserType.STUDENT
    ):
        return redirect("landingpage:index")

    try:
        error_count_rec = None
        user = Student.objects.get(username=username)
        recommendations = Recommendation.objects.filter(user_id=user.pk)
        count = recommendations.count()

        if count == RECOMMENDATION_COUNT:
            error_count_rec = (
                "The maximum number of recommendations have been requested!"
            )
            form = None
        elif request.method == "POST":
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
                    {
                        "user": f,
                        "domain": current_site.domain,
                        "uid1": urlsafe_base64_encode(force_bytes(f.pk)),
                    },
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
        context = {
            "form": form,
            "error_count_rec": error_count_rec,
            "recommendations": recommendations,
        }
    except ValueError:
        context = {"form": form}
    return render(request, "recommendation/recommendation_form.html", context)


def recommendation_rating(request, uidb64):
    teacherRecommendation = Recommendation
    try:
        uid1 = force_text(urlsafe_base64_decode(uidb64))
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
        context = {
            "form": form,
            "teacher_recommendation": teacherRecommendation,
            "teacher_pk": urlsafe_base64_encode(force_bytes(teacherRecommendation.pk)),
        }
        return render(request, "recommendation/recommendation_rating.html", context)
    else:
        context = {"completed": 1}
        return render(request, "recommendation/recommendation_rating.html", context)
