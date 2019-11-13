from django.core.exceptions import ValidationError


def validate_not_used_student_email(value):
    # TODO move this out of the method adn resolve import error
    from register.models import Student

    if Student.objects.filter(email_address=value).exists():
        raise ValidationError("Email already in use")
    return value


def validate_not_used_admin_email(value):
    from register.models import Admin_Staff

    if Admin_Staff.objects.filter(email_address=value).exists():
        raise ValidationError("Email already in use")
    return value
