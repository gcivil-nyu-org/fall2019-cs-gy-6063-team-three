from django.db import models
from django.core import validators
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

from register.models import Student
from high_school.models import HighSchool, Program


GENDER = [("", "Gender"), ("M", "Male"), ("F", "Female")]
APPLICATION_STATUS = ["Rejected", "Accepted", "Submitted", "Withdrawn"]


class HighSchoolApplication(models.Model):
    application_number = models.CharField(max_length=20)
    user = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="high_school_app_user"
    )
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email_address = models.EmailField(
        max_length=50, validators=[validators.validate_email], verbose_name="Email ID"
    )
    phoneNumber = models.CharField(max_length=15, verbose_name="Phone Number")
    address = models.CharField(max_length=100, verbose_name="Address")
    gender = models.CharField(max_length=15, verbose_name="Gender")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("4.00")),
        ],
        verbose_name="GPA",
        default=Decimal("0.00"),
        blank=True,
    )
    parent_name = models.CharField(max_length=100, verbose_name="Parent/Guardian Name")
    parent_phoneNumber = models.CharField(
        max_length=15, verbose_name="Parent/Guardian Phone Number"
    )
    school = models.ForeignKey(
        HighSchool,
        on_delete=models.CASCADE,
        related_name="app_school",
        verbose_name="School",
        blank=True,
        null=True,
    )
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, verbose_name="Program", blank=True, null=True
    )
    is_draft = models.BooleanField(default=True)
    submitted_date = models.DateTimeField(verbose_name="Submitted")
    application_status = models.IntegerField(
        default=2, verbose_name="Application Status"
    )  # 2 = "pending"; 1 = "accepted"; 0 ="rejected"

    def get_fields(self):
        x = []
        for field in self._meta.fields:
            if field.name not in ["id", "application_number", "user", "is_draft"]:
                if field.name == "gender":
                    try:
                        value = [i[1] for i in GENDER if i[0] == self.gender][0]
                    except Exception:
                        value = field.value_from_object(self)
                elif field.name.startswith("school"):
                    value = str(self.school)
                elif field.name.startswith("program"):
                    value = str(self.program)
                elif field.name == "application_status":
                    value = APPLICATION_STATUS[self.application_status]
                else:
                    value = field.value_from_object(self)
                x.append((field.verbose_name, value))
        return x
