from django.db import models
from django.core import validators
from django.core.validators import MinValueValidator
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField


from register.models import Student


class HighSchoolApplication(models.Model):
    application_number = models.CharField(max_length=10)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(
        max_length=50, validators=[validators.validate_email]
    )
    phoneNumber = PhoneNumberField()
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gpa = models.DecimalField(
        max_digits=3, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    parent_name = models.CharField(max_length=100)
    parent_phoneNumber = PhoneNumberField()
    school = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    is_draft = models.BooleanField(default=True)
    submitted_date = models.DateTimeField()

    def get_fields(self):
        return [
            (field.name, field.value_to_string(self))
            for field in HighSchoolApplication._meta.fields
        ]
