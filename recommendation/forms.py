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


class RecommendationRatingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )

    class Meta:
        model = Recommendation
        exclude = [
            "user",
            "first_name",
            "last_name",
            "email_address",
            "submitted_date",
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
        ]
