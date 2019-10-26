from django.shortcuts import render
from django.views.generic.list import ListView
from sodapy import Socrata

from OneApply.constants import ApiInfo
from .forms import SaveHighSchools
from .serializer import HighSchoolSerializer
from .models import HighSchool

client = Socrata(ApiInfo.API_DOMAIN, ApiInfo.APP_TOKEN)


def save_highschool_data(request):
    if request.method == "POST":
        form = SaveHighSchools(request.POST)
        if form.is_valid():
            limit = form.cleaned_data['limit']
            results = client.get(ApiInfo.API_RESOURCE, select=ApiInfo.LOCAL_FIELD_LIST, limit=limit)
            serializer = HighSchoolSerializer(data=results, many=True)
            if serializer.is_valid():
                response = serializer.save()
                return render(request, 'high_school/index.html', {'response': response})
            else:
                print(serializer.errors)
    else:
        form = SaveHighSchools()
    return render(request, 'high_school/save_high_schools.html', {'form': form})


def home(request):
    is_cached = ('highschool' in request.session)
    if not is_cached:
        results = client.get(ApiInfo.API_RESOURCE, select=ApiInfo.LOCAL_FIELD_LIST, limit=1)
        request.session['highschool'] = results

    response = request.session['highschool']
    return render(request, 'high_school/index.html', {"response": response})


class HighSchoolListView(ListView):
    template_name = 'high_school/index.html'
    model = HighSchool
    context_object_name = "high_schools"
    paginate_by = 5
    ordering = ['school_name']
