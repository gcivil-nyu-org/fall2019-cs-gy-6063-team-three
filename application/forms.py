from django.forms import ModelForm
from django import forms

from .models import HighSchoolApplication
from high_school.models import Program


GENDER = [("", "Gender"), ("M", "Male"), ("F", "Female")]


class HighSchoolApplicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].label = "Gender"

        for field in self.fields.keys():
            value = self.fields[field]
            value.widget.attrs.update({"class": "form-control", "id": field})

        if "school" in self.data:
            try:
                school_id = self.data.get("school")
                self.fields["program"].queryset = Program.objects.filter(
                    high_school_id=school_id
                )
            except (ValueError, TypeError) as e:
                print(e)
                self.fields["program"].queryset = Program.objects.none()

    class Meta:
        model = HighSchoolApplication
        exclude = ["application_number", "user", "submitted_date", "is_draft"]
        widgets = {
            "gender": forms.Select(
                choices=GENDER, attrs={"class": "custom-select mr-sm-2"}
            )
        }
