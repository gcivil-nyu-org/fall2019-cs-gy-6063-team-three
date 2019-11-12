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
    recommendation = models.TextField()
    submitted_date = models.DateTimeField()

    def get_fields(self):
        return [
            (field.name, field.value_to_string(self))
            for field in Recommendation._meta.fields
        ]
