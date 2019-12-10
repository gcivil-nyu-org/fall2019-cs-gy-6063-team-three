from django.forms import ModelForm, ValidationError
from django import forms
from django_select2.forms import Select2Widget
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from .models import HighSchoolApplication, GENDER
from high_school.models import HighSchool, Program


class HighSchoolApplicationForm(ModelForm):
    school0 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=True,
    )
    program0 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=True
    )
    school1 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=False,
    )
    program1 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=False
    )
    school2 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=False,
    )
    program2 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=False
    )
    school3 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=False,
    )
    program3 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=False
    )
    school4 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=False,
    )
    program4 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=False
    )
    school5 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=False,
    )
    program5 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=False
    )
    school6 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=False,
    )
    program6 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=False
    )
    school7 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=False,
    )
    program7 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=False
    )
    school8 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=False,
    )
    program8 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=False
    )
    school9 = forms.ModelChoiceField(
        label="School",
        widget=Select2Widget,
        queryset=HighSchool.objects.all(),
        required=False,
    )
    program9 = forms.ModelChoiceField(
        label="Program", queryset=Program.objects.all(), required=False
    )
    confirmation = forms.BooleanField(
        required=False, initial=False, widget=forms.CheckboxInput()
    )

    def __init__(self, *args, **kwargs):
        if "max_count" in kwargs:
            max_count = kwargs.pop("max_count")
        else:
            max_count = 0
        if "user" in kwargs:
            user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["gender"].label = "Gender"
        self.fields["date_of_birth"].label = "Date of Birth"
        self.fields["phoneNumber"].label = "Phone Number"
        self.fields["gpa"].label = "GPA"
        self.fields["parent_phoneNumber"].label = "Parent/Guardian Phone Number"

        self.max_count = max_count
        self.user = user

        for i in range(0, max_count):
            # set initial values of form fields
            self.data = self.initial
            self.fields["school" + str(i)].queryset = self.user.fav_schools.all()
            self.fields["program" + str(i)].queryset = Program.objects.none()
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

        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "id": field}
            )
            if field == "date_of_birth":
                self.fields[field].widget.attrs.update({"placeholder": "yyyy-mm-dd"})
            if field == "confirmation":
                self.fields[field].widget.attrs.update(
                    {"class": "custom-control-input", "id": field}
                )

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
        for i in range(0, 10):
            x.append((self["school" + str(i)], self["program" + str(i)]))
        return x

    def clean_phoneNumber(self):
        phone = self.cleaned_data["phoneNumber"]
        if phone and len(phone) != 14:
            raise ValidationError("Invalid phone number")
        return phone

    def clean_parent_phoneNumber(self):
        phone = self.cleaned_data["parent_phoneNumber"]
        if phone and len(phone) != 14:
            raise ValidationError("Invalid phone number")
        return phone

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
            "email_address": forms.EmailInput(
                attrs={
                    "type": "email",
                    "pattern": "[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,}$",
                    "title": "Invalid email",
                    "placeholder": "student@university.edu",
                }
            ),
        }
