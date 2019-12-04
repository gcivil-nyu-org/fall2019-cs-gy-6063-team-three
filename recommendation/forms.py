from django import forms
from django.forms import ModelForm, ValidationError
from .models import Recommendation, Student


class RecommendationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )

    def clean_email_address(self):
        email = self.cleaned_data["email_address"]
        if Student.objects.filter(email_address=email).exists():
            raise ValidationError("Recommendation email cannot belong to a student")
        return email

    class Meta:
        model = Recommendation
        exclude = [
            "user",
            "submitted_date",
            "known_length",
            "known_strength",
            "known_location",
            "rating_concepts",
            "rating_creativity",
            "rating_mathematical",
            "rating_written",
            "rating_oral",
            "rating_goals",
            "rating_socialization",
            "rating_analyzing",
            "rating_comment",
        ]


STRENGTH_CHOICES = [(0, "Casually"), (1, "Well"), (2, "Very Well")]
LOCATION_CHOICES = [
    (0, "Teacher in One Class"),
    (1, "Teacher in Multiple Classes"),
    (2, "Advisor"),
    (3, "Mentor"),
    (4, "Other"),
]
GENERAL_CHOICES = [
    (1, ""),
    (2, ""),
    (3, ""),
    (4, ""),
    (5, ""),
    (6, ""),
    (7, ""),
    (0, ""),
]


class RecommendationRatingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if field.widget.template_name is forms.widgets.RadioSelect.template_name:
                field.widget.attrs.update(
                    {"class": "radio", "placeholder": field.label}
                )
            else:
                field.widget.attrs.update(
                    {"class": "form-control", "placeholder": field.label}
                )

    known_strength = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=STRENGTH_CHOICES
    )
    known_location = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=LOCATION_CHOICES
    )
    rating_concepts = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=GENERAL_CHOICES
    )
    rating_creativity = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=GENERAL_CHOICES
    )
    rating_mathematical = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=GENERAL_CHOICES
    )
    rating_written = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=GENERAL_CHOICES
    )
    rating_oral = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENERAL_CHOICES)
    rating_goals = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=GENERAL_CHOICES
    )
    rating_socialization = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=GENERAL_CHOICES
    )
    rating_analyzing = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=GENERAL_CHOICES
    )

    class Meta:
        model = Recommendation
        exclude = ["user", "first_name", "last_name", "email_address", "submitted_date"]
