from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from sodapy import Socrata

from OneApply.constants import ApiInfo, UserType
from .forms import SaveHighSchoolsForm
from .serializer import HighSchoolSerializer
from .models import HighSchool
from register.models import Student

client = Socrata(ApiInfo.API_DOMAIN, ApiInfo.APP_TOKEN)


def save_highschool_data(request):
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


def get_user(request):
    context = {}
    is_login = request.session.get("is_login", None)
    if not is_login:
        return redirect("landingpage:index")
    user_name = request.session.get("username", None)
    user_type = request.session.get("user_type", None)
    is_valid_user = False
    if not user_name or user_type != UserType.STUDENT:
        context["unauth"] = True
        context["high_schools"] = None
        context["selected_school"] = None
        context["empty_list"] = None
    user = None
    try:
        user = Student.objects.get(username=user_name)
        is_valid_user = True
    except Student.DoesNotExist:
        context["unauth"] = True
        context["high_schools"] = None
        context["selected_school"] = None
        context["empty_list"] = None

    return is_valid_user, user, user_type, context


class HighSchoolListView(ListView):
    template_name = "high_school/index.html"
    model = HighSchool
    context_object_name = "high_schools"
    # paginator_class = None
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_type = None
        self.user = None
        self.dbn = None
        self.query = None
        self.loc_filter = {}
        self.is_fav_on = 0

    def get(self, *args, **kwargs):
        if not self.request.session.get("is_login", None):
            return redirect("landingpage:index")
        return super(HighSchoolListView, self).get(*args, **kwargs)

    def get_queryset(self):
        if "dbn" in self.kwargs:
            self.dbn = self.kwargs["dbn"]
        self.query = self.request.GET.get("query")
        self.loc_filter["X"] = self.request.GET.get("loc_bx")
        self.loc_filter["K"] = self.request.GET.get("loc_bk")
        self.loc_filter["M"] = self.request.GET.get("loc_mn")
        self.loc_filter["Q"] = self.request.GET.get("loc_qn")
        self.loc_filter["R"] = self.request.GET.get("loc_si")
        if self.request.GET.get("is_fav_on"):
            self.is_fav_on = int(self.request.GET.get("is_fav_on"))
        else:
            self.is_fav_on = 0
        is_valid_user, temp_user, temp_user_type, temp_context = get_user(self.request)
        if not is_valid_user:
            self.user = None
            return None
        else:
            self.user = temp_user
            self.user_type = temp_user_type
        return self.getHighSchools()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HighSchoolListView, self).get_context_data(**kwargs)

        if not self.user:
            context["unauth"] = True
            context["high_schools"] = None
            context["selected_school"] = None
            context["empty_list"] = None
        else:
            context["unauth"] = False
            if not context["high_schools"]:
                context["empty_list"] = True
            else:
                if self.dbn:
                    context["selected_school"] = get_object_or_404(
                        HighSchool, dbn=self.dbn
                    )
                else:
                    context["selected_school"] = None
                context["fav_schools"] = self.get_fav_schools()
                context["empty_list"] = False

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
        elif self.is_fav_on and self.is_fav_on == 1:
            high_schools = self.get_fav_schools()
        else:
            high_schools = HighSchool.objects.order_by("school_name")

        return high_schools

    def get_fav_schools(self):
        return self.user.fav_schools.all()


def update_fav_hs(request, school_dbn, is_fav):
    high_school = None
    try:
        high_school = HighSchool.objects.get(dbn=school_dbn)
    except HighSchool.DoesNotExist:
        # Todo : this needs to be changed once function is moved to HighSchoolListView
        pass

    is_valid_user, temp_user, temp_user_type, temp_context = get_user(request)
    if is_valid_user:
        user = temp_user
        if user.__class__ is Student:
            if is_fav == 1:
                user.fav_schools.add(high_school)
                user.save()
            else:
                # user.fav_schools.clear()
                print(high_school.student_set.all())
                user.fav_schools.remove(high_school)
                user.save()

    return redirect('dashboard:high_school:index')
