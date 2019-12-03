from django.contrib import admin
from django.conf.urls import url
from functools import update_wrapper
from django.template.response import TemplateResponse
from django.conf import settings
from sodapy import Socrata

from OneApply.constants import ApiInfo
from .serializer import HighSchoolSerializer
from .forms import SaveHighSchoolsForm
from .models import HighSchool, Program

client = Socrata(ApiInfo.API_DOMAIN, ApiInfo.APP_TOKEN)


class HighSchoolAdmin(admin.ModelAdmin):
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        # get the default urls
        urls = super().get_urls()
        # define custom urls
        my_urls = [
            url(r"^save_hs/$", wrap(self.save_hs_view), name="save_high_schools")
        ]
        return my_urls + urls

    def save_hs_view(self, request):
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
        )
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
                    context["response"] = "High Schools saved successfully."
                    context["errors"] = None
                    context["response"] += "\n" + save_programs(limit)
        else:
            form = SaveHighSchoolsForm()
        context["form"] = form
        return TemplateResponse(request, "high_school/save_high_schools.html", context)


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
    if results:
        for result in results:
            parse_result(result)
        return "Programs saved successfully."
    else:
        return "Programs not saved."


admin.site.register(HighSchool, HighSchoolAdmin)
admin.site.register(Program)
