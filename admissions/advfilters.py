import django_filters

from application.models import HighSchoolApplication

FILTER_CHOICES = (("0", "Rejected"), ("1", "Accepted"), ("2", "Pending"))


class ApplicationFilter(django_filters.FilterSet):
    gpa = django_filters.NumericRangeFilter(
        field_name="gpa", label="GPA (Between)", lookup_expr="range"
    )

    application_number = django_filters.CharFilter(
        field_name="application_number",
        lookup_expr="icontains",
        label="Application Number",
    )
    first_name = django_filters.CharFilter(
        field_name="first_name", lookup_expr="icontains", label="First Name"
    )
    last_name = django_filters.CharFilter(
        field_name="last_name", lookup_expr="icontains", label="Last Name"
    )
    application_status = django_filters.ChoiceFilter(
        field_name="application_status",
        label="Application Status",
        choices=FILTER_CHOICES,
    )

    class Meta:
        model = HighSchoolApplication
        fields = [
            "gpa",
            "application_number",
            "first_name",
            "last_name",
            "application_status",
            "program",
        ]
