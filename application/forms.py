from django.forms import ModelForm
from django import forms

from .models import HighSchoolApplication


GENDER = [("", "Gender"), ("M", "Male"), ("F", "Female")]


class HighSchoolApplicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].label = "Gender"

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = HighSchoolApplication
        exclude = ["application_number", "user", "submitted_date", "is_draft"]
        widgets = {
            "gender": forms.Select(
                choices=GENDER, attrs={"class": "custom-select mr-sm-2"}
            )
        }
