from django.core.exceptions import ValidationError


def validate_not_used_email(value):
    from register.models import Student, Admin_Staff
    if Student.objects.filter(email_address=value).exists() or Admin_Staff.objects.filter(email_address=value).exists():
        raise ValidationError("Email already in use")
    return value

