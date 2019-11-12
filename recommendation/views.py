from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import RecommendationForm
from .models import Recommendation
from django.urls import reverse


def new_recommendation(request):
    if request.method == "POST":
        # TODO user_id will be replaced by sessions
        user_id = 2
        form = RecommendationForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = user_id
            f.save()
            return HttpResponseRedirect(reverse("recommendation:index"))
    else:
        form = RecommendationForm()
    context = {"form": form}
    return render(request, "recommendation/recommendation_form.html", context)


def all_recommendation(request, user_type):
    # TODO user_id will be replaced by sessions
    user_id = 2
    context = {"recommendations": Recommendation.objects.filter(user_id=user_id)}
    return render(request, "recommendation/index.html", context)
