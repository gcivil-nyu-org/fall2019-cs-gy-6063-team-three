from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from sodapy import Socrata

from OneApply.constants import ApiInfo
from .forms import SaveHighSchoolsForm
from .serializer import HighSchoolSerializer
from .models import HighSchool

client = Socrata(ApiInfo.API_DOMAIN, ApiInfo.APP_TOKEN)


def save_highschool_data(request, user_type):
    if request.method == "POST":
        form = SaveHighSchoolsForm(request.POST)
        if form.is_valid():
            limit = form.cleaned_data["limit"]
            results = client.get(
                ApiInfo.API_RESOURCE, select=ApiInfo.LOCAL_FIELD_LIST, limit=limit
            )
            serializer = HighSchoolSerializer(data=results, many=True)
            if serializer.is_valid():
                response = serializer.save()
                return render(request, "high_school/index.html", {"response": response})
            else:
                print(serializer.errors)
    else:
        form = SaveHighSchoolsForm()
    return render(request, "high_school/save_high_schools.html", {"form": form})


class HighSchoolListView(ListView):
    template_name = "high_school/index.html"
    model = HighSchool
    context_object_name = "high_schools"
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dbn = None
        self.query = None

    def get_queryset(self):
        if "dbn" in self.kwargs:
            self.dbn = self.kwargs["dbn"]
        self.query = self.request.GET.get("q")
        """if query:
            return HighSchool.objects.filter(school_name__icontains=query).order_by(
                "school_name"
            )  # noqa: E501
        else:"""
        return HighSchool.objects.order_by("school_name")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HighSchoolListView, self).get_context_data(**kwargs)
        # TODO: add check for aunthorized access
        # check for both -> user not None and user instance of Student
        # redirection happens by setting "unauthorized" to True
        # context['unauthorized'] = True
        if self.dbn:
            context["selected_school"] = get_object_or_404(HighSchool, dbn=self.dbn)
        if self.query:
            context["high_schools"] = HighSchool.objects.filter(
                school_name__icontains=self.query
            ).order_by(
                "school_name"
            )  # noqa: E501
        return context
