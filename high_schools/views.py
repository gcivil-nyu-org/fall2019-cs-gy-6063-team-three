from django.shortcuts import render
from django.views.generic.detail import DetailView
from sodapy import Socrata

from OneApply.constants import ApiInfo
from .models import HighSchools

client = Socrata(ApiInfo.API_DOMAIN, ApiInfo.APP_TOKEN)


# class HighSchoolDetailView(DetailView):
#     model = HighSchools
#
#     def get_context_data(self, **kwargs):
#         context = client.get(ApiInfo.API_RESOURCE, select=ApiInfo.LOCAL_FIELD_LIST, limit=1)
#         return context


def home(request):
    is_cached = ('highschool' in request.session)
    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        results = client.get(ApiInfo.API_RESOURCE, select=ApiInfo.LOCAL_FIELD_LIST, limit=1)
        request.session['highschool'] = results

    response = request.session['highschool']
    return render(request, 'high_schools/index.html', {"response": response})
