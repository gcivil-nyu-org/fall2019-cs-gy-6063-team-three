from django.db import models
from django.core import validators
from django.core.validators import RegexValidator


PHONE_REGEX = "r'^([0-9]{3}) [0-9]{3}-[0-9]{4}$'"


def auto_str(cls):
    def __str__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )

    cls.__str__ = __str__
    return cls


class User(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email_address = models.EmailField(
        max_length=200, null=True, blank=False, validators=[validators.validate_email]
    )
    phoneNumber = models.CharField(
        max_length=15, validators=[RegexValidator(PHONE_REGEX)]
    )
    username = models.CharField(max_length=20, null=True, blank=False)
    password = models.CharField(max_length=256)

    class Meta:
        abstract = True


@auto_str
class Student(User):
    current_school = models.CharField(max_length=100, null=True, blank=True)
    borough = models.CharField(max_length=2)


@auto_str
class Admin_Staff(User):
    school = models.CharField(max_length=100, null=True, blank=True)
    supervisor_email = models.EmailField(max_length=100, null=True, blank=True)
