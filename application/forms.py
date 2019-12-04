from django.forms import ModelForm, ValidationError
from django import forms
from django_select2.forms import Select2Widget
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from .models import HighSchoolApplication, GENDER
from high_school.models import HighSchool, Program


class HighSchoolApplicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if "max_count" in kwargs:
            max_count = kwargs.pop("max_count")
        else:
            max_count = 0
        super().__init__(*args, **kwargs)
        self.fields["gender"].label = "Gender"
        self.fields["date_of_birth"].label = "Date of Birth"
        self.fields["phoneNumber"].label = "Phone Number"
        self.fields["gpa"].label = "GPA"
        self.fields["parent_phoneNumber"].label = "Parent/Guardian Phone Number"

        self.max_count = max_count

        for i in range(0, max_count):
            self.fields["school" + str(i)] = forms.ModelChoiceField(
                label="School",
                widget=Select2Widget,
                queryset=HighSchool.objects.all(),
                required=False,
            )
            self.fields["program" + str(i)] = forms.ModelChoiceField(
                label="Program", queryset=Program.objects.none(), required=False
            )

            # set initial values of form fields
            self.data = self.initial
            if "school" + str(i) in self.data:
                try:
                    school_id = self.data.get("school" + str(i), None)
                    prog_id = self.data.get("program" + str(i), None)
                    if prog_id:
                        self.fields[
                            "program" + str(i)
                        ].queryset = Program.objects.filter(pk=prog_id)
                    else:
                        self.fields[
                            "program" + str(i)
                        ].queryset = Program.objects.filter(high_school_id=school_id)
                except (ValueError, TypeError):
                    self.fields["program" + str(i)].queryset = Program.objects.none()
            else:
                self.fields["program" + str(i)].queryset = Program.objects.none()

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

    def get_school_prog_fields(self):
        x = []
        for i in range(0, self.max_count):
            x.append((self["school" + str(i)], self["program" + str(i)]))
        return x

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
            "gender": forms.Select(choices=GENDER),
            "date_of_birth": forms.DateInput(
                format="%m-%d-%Y",
                attrs={
                    "type": "date",
                    "max": (datetime.now() - relativedelta(years=11)).strftime(
                        "%Y-%m-%d"
                    ),
                    "min": (datetime.now() - relativedelta(years=15)).strftime(
                        "%Y-%m-%d"
                    ),
                },
            ),
            "gpa": forms.NumberInput(
                attrs={"type": "number", "max": 4.00, "min": 0.00, "step": 0.01}
            ),
        }
