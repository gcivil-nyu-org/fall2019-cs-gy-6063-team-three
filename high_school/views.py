from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from sodapy import Socrata

from OneApply.constants import ApiInfo, UserType
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
            for x in range(limit):
                # for testing purposes, we should not be using actual high school emails
                # all school emails are replaced with Patryk's email for future implementation of # noqa : E501
                # supervisor email being taken directly from the school.
                serializer.initial_data[x]["school_email"] = "pp2224@nyu.edu"
                try:
                    # check if there is a start time in the school info
                    # if it is there then get the substring that ends it after "am"
                    # some fields have text after the time that is not necessary
                    if serializer.initial_data[x]["start_time"]:
                        am_loc = serializer.initial_data[x]["start_time"].find("am")
                        serializer.initial_data[x][
                            "start_time"
                        ] = serializer.initial_data[x]["start_time"][: am_loc + 2]
                except KeyError:
                    # if there is no start time provided in the info set it to N/A
                    serializer.initial_data[x]["start_time"] = "N/A"
                try:
                    # check if there is a end time in the school info
                    # if it is there then get the substring that ends it after "pm"
                    # some fields have text after the time that is not necessary
                    if serializer.initial_data[x]["end_time"]:
                        pm_loc = serializer.initial_data[x]["end_time"].find("pm")
                        serializer.initial_data[x][
                            "end_time"
                        ] = serializer.initial_data[x]["end_time"][: pm_loc + 2]
                except KeyError:
                    # if there is no end time provided in the info set it to N/A
                    serializer.initial_data[x]["end_time"] = "N/A"
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
        self.user_type = None
        self.dbn = None
        self.query = None
        self.loc_filter = {}

    def get(self, *args, **kwargs):
        if not self.request.session.get("is_login", None):
            return redirect("landingpage:index")
        return super(HighSchoolListView, self).get(*args, **kwargs)

    def get_queryset(self):
        if "dbn" in self.kwargs:
            self.dbn = self.kwargs["dbn"]
        self.query = self.request.GET.get("q")
        self.loc_filter["X"] = self.request.GET.get("loc_bx")
        self.loc_filter["K"] = self.request.GET.get("loc_bk")
        self.loc_filter["M"] = self.request.GET.get("loc_mn")
        self.loc_filter["Q"] = self.request.GET.get("loc_qn")
        self.loc_filter["R"] = self.request.GET.get("loc_si")
        return HighSchool.objects.order_by("school_name")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HighSchoolListView, self).get_context_data(**kwargs)
        user_type = self.request.session.get("user_type", None)
        if not user_type:
            return redirect("landingpage:index")
        if user_type != UserType.STUDENT:
            context["unauth"] = True
            context["high_schools"] = None
            context["selected_school"] = None
            context["empty_list"] = False
        else:
            context["unauth"] = False
            if self.dbn:
                context["selected_school"] = get_object_or_404(HighSchool, dbn=self.dbn)
            else:
                context["selected_school"] = None

            high_schools = self.getHighSchools()
            if high_schools:
                context["high_schools"] = high_schools
                context["empty_list"] = False
            else:
                context["high_schools"] = None
                context["empty_list"] = True

        return context

    def getHighSchools(self):
        high_schools = None
        borough_filter = ""
        for boro in self.loc_filter:
            if self.loc_filter[boro]:
                borough_filter += boro + " , "
        borough_filter = borough_filter[:-3]

        if self.query:
            if borough_filter:
                high_schools = HighSchool.objects.filter(
                    school_name__icontains=self.query, boro__in=borough_filter
                ).order_by(
                    "school_name"
                )  # noqa: E501
            else:
                high_schools = HighSchool.objects.filter(
                    school_name__icontains=self.query
                ).order_by("school_name")
        elif borough_filter:
            high_schools = HighSchool.objects.filter(boro__in=borough_filter).order_by(
                "school_name"
            )
        else:
            high_schools = HighSchool.objects.order_by("school_name")
        return high_schools
