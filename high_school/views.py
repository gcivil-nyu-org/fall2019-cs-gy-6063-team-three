from django.shortcuts import redirect
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from OneApply.constants import UserType
from high_school.models import Program
from .models import HighSchool
from register.models import Student


def get_user(request):
    context = {}
    is_login = request.session.get("is_login", None)
    if not is_login:
        return False, None, None, None
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
        is_valid_user, temp_user, temp_user_type, temp_context = get_user(self.request)
        if not is_valid_user:
            self.user = None
            return redirect("landingpage:index")
        else:
            self.user = temp_user
            self.user_type = temp_user_type
        return super(HighSchoolListView, self).get(*args, **kwargs)

    def get_queryset(self):
        if "dbn" in self.kwargs:
            self.dbn = self.kwargs["dbn"]
        self.search_filter_params = self.setup_params()
        return self.get_high_schools()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HighSchoolListView, self).get_context_data(**kwargs)

        # a valid user should always exist at this point in the view lifecycle
        # validation check for valid user happens in 'get'
        if self.user:
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
                context["fav_schools"] = self.get_fav_schools()
            context["search_filter_params"] = self.search_filter_params
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
                    (
                        Q(school_name__icontains=self.query)
                        | Q(location__icontains=self.query)
                        | Q(program__name__icontains=self.query)
                    )
                    & Q(boro__in=borough_filter)
                ).distinct()
            elif high_schools:
                high_schools = (
                    high_schools.filter(
                        (
                            Q(school_name__icontains=self.query)
                            | Q(location__icontains=self.query)
                            | Q(program__name__icontains=self.query)
                        )
                    )
                    .distinct()
                    .order_by("school_name")
                )
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


@api_view(["POST"])
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
                response["status"] = 200
                response["message"] = "Success"
            else:
                response["status"] = 403
                response["message"] = "Forbidden - invalid user"
        else:
            response["status"] = 404
            response["message"] = "No matching high school found"

    return Response(response)
