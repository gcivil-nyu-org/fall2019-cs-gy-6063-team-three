from django.db import models
from django.core import validators
from django.core.validators import RegexValidator
from datetime import datetime
from register.models import Student

PHONE_REGEX = "r'^([1-9]{1}\\d{2}) \\d{3} -\\d{4}'"


def auto_str(cls):
    def __str__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )

    cls.__str__ = __str__
    return cls


@auto_str
class HighSchoolApplication(models.Model):
    application_number = models.IntegerField()
    user_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(
        max_length=50, validators=[validators.validate_email]
    )
    phoneNumber = models.CharField(
        max_length=15, validators=[RegexValidator(PHONE_REGEX)],
    )
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    parent_name = models.CharField(max_length=100)
    parent_phoneNumber = models.CharField(
        max_length=15, validators=[RegexValidator(PHONE_REGEX)],
    )
    school_id = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    submitted_date = models.DateTimeField(default=datetime.now)
