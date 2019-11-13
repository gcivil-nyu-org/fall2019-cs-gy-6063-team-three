from django.shortcuts import render, redirect
from django.views.generic import ListView
from sodapy import Socrata

from OneApply.constants import ApiInfo, UserType
from high_school.models import Program
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
            response = save_high_schools(limit)
            if response:
                save_programs(limit)
            return render(request, "high_school/index.html", {"response": response})

    else:
        form = SaveHighSchoolsForm()
    return render(request, "high_school/save_high_schools.html", {"form": form})


def save_high_schools(limit):
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
                serializer.initial_data[x]["start_time"] = serializer.initial_data[x][
                    "start_time"
                ][: am_loc + 2]
        except KeyError:
            # if there is no start time provided in the info set it to N/A
            serializer.initial_data[x]["start_time"] = "N/A"
        try:
            # check if there is a end time in the school info
            # if it is there then get the substring that ends it after "pm"
            # some fields have text after the time that is not necessary
            if serializer.initial_data[x]["end_time"]:
                pm_loc = serializer.initial_data[x]["end_time"].find("pm")
                serializer.initial_data[x]["end_time"] = serializer.initial_data[x][
                    "end_time"
                ][: pm_loc + 2]
        except KeyError:
            # if there is no end time provided in the info set it to N/A
            serializer.initial_data[x]["end_time"] = "N/A"
    if serializer.is_valid():
        return serializer.save()
    else:
        print(serializer.errors)
        return None


def extract_offer_rate(offer_rate_data):
    if not offer_rate_data or offer_rate_data[0] != "-":
        return 0
    # Offer rate in the dataset is like:
    # -96% of offers went to this group
    return offer_rate_data.split("%")[0][1:]


def parse_result(result):
    for i in range(1, 11):
        code = "code" + str(i)
        seats = "seats9ge" + str(i)
        program_name = "program" + str(i)
        description = "prgdesc" + str(i)
        offer_rate = "offer_rate" + str(i)
        if (
            result.get(code)
            and Program.objects.filter(code=result.get(code)).count() == 0
        ):
            # This result is a valid program, and not already in DB save it.
            program = Program()
            # TODO: change following statement to
            program.high_school = HighSchool.objects.get(dbn=result.get("dbn"))
            #  once the school model has dbn as unique/PK
            # program.high_school = HighSchool.objects.filter(dbn=result.get("dbn"))[0]
            program.code = result.get(code)
            program.name = result.get(program_name)
            program.description = result.get(description)
            try:
                seats = int(result.get(seats, 0))
            except ValueError:
                seats = 0
            program.number_of_seats = seats
            program.offer_rate = extract_offer_rate(result.get(offer_rate))
            program.save()


def save_programs(limit):
    results = client.get(
        ApiInfo.API_RESOURCE, select=ApiInfo.LOCAL_PROGRAM_FIELD_LIST, limit=limit
    )
    for result in results:
        parse_result(result)


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
        self.is_fav_empty = True

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
            context["empty_list"] = 0
            if not context["high_schools"]:
                context["empty_list"] = 1
                if self.is_fav_empty and self.is_fav_on:
                    context["empty_list"] = 2
            else:
                if self.dbn:
                    selected_school = HighSchool.objects.filter(dbn=self.dbn)
                    if selected_school:
                        context["selected_school"] = selected_school[0]
                    else:
                        context["selected_school"] = None
                        context["high_schools"] = None
                        context["empty_list"] = 1
                else:
                    context["selected_school"] = None
                context["fav_schools"] = self.get_fav_schools()

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
        fav_schools = self.user.fav_schools.all()
        if not fav_schools:
            self.is_fav_empty = True
        return fav_schools


def update_fav_hs(request, school_dbn, is_fav):
    try:
        high_school = HighSchool.objects.get(dbn=school_dbn)
    except HighSchool.DoesNotExist:
        pass
    else:
        if high_school:
            is_valid_user, temp_user, temp_user_type, temp_context = get_user(request)
            if is_valid_user:
                user = temp_user
                if user.__class__ is Student:
                    if is_fav == 1:
                        user.fav_schools.add(high_school)
                        user.save()
                    else:
                        user.fav_schools.remove(high_school)
                        user.save()

    return redirect("dashboard:high_school:index")
