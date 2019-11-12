from django.forms import ModelForm

from .models import Recommendation


class RecommendationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )

    class Meta:
        model = Recommendation
        exclude = ["student", "recommendation", "submitted_date"]
