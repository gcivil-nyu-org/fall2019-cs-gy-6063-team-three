from django.db import models
from django.core import validators

from register.models import Student


class Recommendation(models.Model):
    user = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_recommending"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(
        max_length=50, validators=[validators.validate_email]
    )
    known_length = models.IntegerField(null=True)
    known_strength = models.IntegerField(null=True)
    known_location = models.IntegerField(null=True)
    rating_concepts = models.IntegerField(null=True)
    rating_creativity = models.IntegerField(null=True)
    rating_mathematical = models.IntegerField(null=True)
    rating_written = models.IntegerField(null=True)
    rating_oral = models.IntegerField(null=True)
    rating_goals = models.IntegerField(null=True)
    rating_socialization = models.IntegerField(null=True)
    rating_analyzing = models.IntegerField(null=True)
    submitted_date = models.DateTimeField(null=True)

    def get_fields(self):
        return [
            (field.name, field.value_to_string(self))
            for field in Recommendation._meta.fields
        ]
