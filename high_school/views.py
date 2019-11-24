from django.shortcuts import render, redirect
from django.views.generic import ListView
from sodapy import Socrata
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
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
            response, errors = save_high_schools(limit)
            context = {}
            if errors:
                context["response"] = "Errors"
                context["errors"] = errors
            elif response:
                context["response"] = response
                context["errors"] = None
                save_programs(limit)
            return render(request, "high_school/index.html", context)

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
        return serializer.save(), None
    else:
        if settings.DEBUG:
            print(serializer.errors)
        return None, serializer.errors


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
            program.high_school = HighSchool.objects.get(dbn=result.get("dbn"))
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
    user = None
    if not user_name or user_type != UserType.STUDENT:
        context["unauth"] = True
        context["high_schools"] = None
        context["selected_school"] = None
        context["empty_list"] = None
    else:
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
        self.search_filter_params = {}

    def get(self, *args, **kwargs):
        if not self.request.session.get("is_login", None):
            return redirect("landingpage:index")
        return super(HighSchoolListView, self).get(*args, **kwargs)

    def get_queryset(self):
        if "dbn" in self.kwargs:
            self.dbn = self.kwargs["dbn"]
        self.search_filter_params = self.setup_params()
        is_valid_user, temp_user, temp_user_type, temp_context = get_user(self.request)
        if not is_valid_user:
            self.user = None
        else:
            self.user = temp_user
            self.user_type = temp_user_type
        return self.get_high_schools()

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
                        context["selected_school_programs"] = self.get_hs_programs(
                            selected_school[0]
                        )
                    else:
                        context["selected_school"] = None
                        context["selected_school_programs"] = None
                        context["high_schools"] = None
                        context["empty_list"] = 1
                else:
                    context["selected_school"] = None
                context["search_filter_params"] = self.search_filter_params
                context["fav_schools"] = self.get_fav_schools()

        return context

    def get_high_schools(self):
        borough_filter = ""
        for boro in self.loc_filter:
            if self.loc_filter[boro]:
                borough_filter += boro + " , "
        borough_filter = borough_filter[:-3]

        if self.is_fav_on and self.is_fav_on == 1:
            high_schools = self.get_fav_schools()
        else:
            high_schools = HighSchool.objects.order_by("school_name")

        if self.query:
            if borough_filter and high_schools:
                high_schools = high_schools.filter(
                    school_name__icontains=self.query, boro__in=borough_filter
                )  # noqa: E501
            elif high_schools:
                high_schools = high_schools.filter(
                    school_name__icontains=self.query
                ).order_by("school_name")
        elif borough_filter and high_schools:
            high_schools = high_schools.filter(boro__in=borough_filter)

        return high_schools

    def get_fav_schools(self):
        fav_schools = self.user.fav_schools.all()
        if not fav_schools:
            self.is_fav_empty = True
        return fav_schools

    def get_hs_programs(self, selected_school):
        if selected_school:
            return Program.objects.filter(high_school=selected_school.dbn)

    def setup_params(self):
        obj = self.get_param_obj(self.request.GET)
        self.query = obj.get("query")
        self.loc_filter["X"] = obj.get("borough").get("loc_bx")
        self.loc_filter["K"] = obj.get("borough").get("loc_bk")
        self.loc_filter["M"] = obj.get("borough").get("loc_mn")
        self.loc_filter["Q"] = obj.get("borough").get("loc_qn")
        self.loc_filter["R"] = obj.get("borough").get("loc_si")
        if obj.get("is_fav_on"):
            self.is_fav_on = 1
        else:
            self.is_fav_on = 0

        return obj

    def get_param_obj(self, get_obj):
        obj = {"filter_count": 0, "borough": {}}
        if get_obj.get("query"):
            obj["query"] = get_obj.get("query")

        if get_obj.get("is_fav_on"):
            obj["is_fav_on"] = get_obj.get("is_fav_on")

        if get_obj.get("loc_all"):
            obj["borough"]["loc_all"] = "on"
            obj["filter_count"] += 1
        else:
            if get_obj.get("loc_bx"):
                obj["borough"]["loc_bx"] = get_obj.get("loc_bx")
                obj["filter_count"] += 1
            if get_obj.get("loc_bk"):
                obj["borough"]["loc_bk"] = get_obj.get("loc_bk")
                obj["filter_count"] += 1
            if get_obj.get("loc_mn"):
                obj["borough"]["loc_mn"] = get_obj.get("loc_mn")
                obj["filter_count"] += 1
            if get_obj.get("loc_qn"):
                obj["borough"]["loc_qn"] = get_obj.get("loc_qn")
                obj["filter_count"] += 1
            if get_obj.get("loc_si"):
                obj["borough"]["loc_si"] = get_obj.get("loc_si")
                obj["filter_count"] += 1

        if obj["filter_count"] == 0 or not obj["borough"]:
            obj["borough"]["loc_all"] = "on"
            obj["filter_count"] += 1
        return obj


@api_view(['POST'])
def update_fav_hs(request, school_dbn, is_fav):
    response = {}
    if request.method == "POST":
        try:
            high_school = HighSchool.objects.get(dbn=school_dbn)
        except HighSchool.DoesNotExist:
            high_school = None
        if high_school:
            is_valid_user, user, _, _ = get_user(request)
            if is_valid_user:
                if is_fav == 1:
                    user.fav_schools.add(high_school)
                    user.save()
                else:
                    user.fav_schools.remove(high_school)
                    user.save()
                response['status'] = 200
                response['message'] = "Success"
            else:
                response['status'] = 403
                response['message'] = "Forbidden - invalid user"
        else:
            response['status'] = 404
            response['message'] = "No matching high school found"
    else:
        response['status'] = 405
        response['message'] = "Invalid method type"
    return Response(response)
