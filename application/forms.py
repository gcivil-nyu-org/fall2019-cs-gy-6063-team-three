from django.forms import ModelForm
from django import forms

from .models import HighSchoolApplication
from high_school.models import Program


GENDER = [("", "Gender"), ("M", "Male"), ("F", "Female")]


class HighSchoolApplicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if "disable" in kwargs:
            disable = kwargs.pop("disable")
        else:
            disable = False
        super().__init__(*args, **kwargs)
        self.fields["gender"].label = "Gender"
        self.fields["date_of_birth"].label = "Date of birth (yyyy-mm-dd)"
        self.fields["phoneNumber"].label = "Phone number"
        self.fields["gpa"].label = "GPA"
        self.fields["parent_phoneNumber"].label = "Parent phone number"

        for field in self.fields.keys():
            value = self.fields[field]
            value.widget.attrs.update({"class": "form-control", "id": field})

        if "school" in self.data:
            try:
                school_id = self.data.get("school", None)
                self.fields["program"].queryset = Program.objects.filter(
                    high_school_id=school_id
                )
            except (ValueError, TypeError):
                self.fields["program"].queryset = Program.objects.none()
        else:
            self.fields["program"].queryset = Program.objects.none()

        if disable:
            self.fields["school"].widget.attrs["disabled"] = True
            self.fields["program"].widget.attrs["disabled"] = True

    class Meta:
        model = HighSchoolApplication
        exclude = [
            "application_number",
            "user",
            "submitted_date",
            "is_draft",
            "application_status",
        ]
        widgets = {
            "gender": forms.Select(
                choices=GENDER, attrs={"class": "custom-select mr-sm-2"}
            )
        }
