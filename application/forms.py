from django.forms import ModelForm, ValidationError
from django import forms
from django_select2.forms import Select2Widget
from datetime import date
from decimal import Decimal

from .models import HighSchoolApplication, GENDER
from high_school.models import Program


class HighSchoolApplicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if "disable" in kwargs:
            disable = kwargs.pop("disable")
        else:
            disable = False
        super().__init__(*args, **kwargs)
        self.fields["gender"].label = "Gender"
        self.fields["date_of_birth"].label = "Date of Birth"
        self.fields["phoneNumber"].label = "Phone number"
        self.fields["gpa"].label = "GPA"
        self.fields["parent_phoneNumber"].label = "Parent/Guardian Phone number"

        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "id": field}
            )
            if field in ["phoneNumber", "parent_phoneNumber"]:
                self.fields[field].widget.attrs.update(
                    {"placeholder": "Eg: +19998887777"}
                )
            if field == "date_of_birth":
                self.fields[field].widget.attrs.update({"placeholder": "yyyy-mm-dd"})

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

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        if dob is not None:
            today = date.today()
            age = (
                today.year
                - dob.year
                - ((today.month, today.day) < (dob.month, dob.day))
            )
            if age < 11 or age > 15:
                raise ValidationError("Age should be between 11 to 15 years")
        return dob

    def clean_gpa(self):
        gpa = self.cleaned_data["gpa"]
        if gpa is None:
            gpa = Decimal("0.00")
        return gpa

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
            ),
            "school": Select2Widget,
        }
