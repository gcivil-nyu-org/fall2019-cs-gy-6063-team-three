from django.forms import ValidationError
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
import re
from .models import Student, Admin_Staff

BOROUGH_CHOICES = [
    ("", "Borough"),
    ("MN", "Manhattan"),
    ("BK", "Brooklyn"),
    ("QN", "Queens"),
    ("BX", "The Bronx"),
    ("SI", "Staten Island"),
]

REG_EX = (
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&_-]{8,20}$"
)  # noqa: W605, E501


class StudentRegisterForm(ModelForm):
    input_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", "placeholder": field})

        self.fields["confirm_password"].widget.attrs.update(
            {"placeholder": "Password (Once more)"}
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Student.objects.filter(username=username).exists():
            raise ValidationError("Username already in use")
        return username

    def clean_input_password(self):
        input_password = self.cleaned_data["input_password"]
        pattern = re.compile(REG_EX)
        if re.search(pattern, input_password):
            return input_password
        else:
            raise ValidationError(
                "The password should be minimum 8 characters long and should contain "
                "at least 1 of each\nUppercase, Lowercase, 1digit, 1 symbol(@#$%^&+=_-)"
            )

    def clean_confirm_password(self):
        if "input_password" not in self.cleaned_data:
            return ValidationError("Password not valid")
        input_password = self.cleaned_data["input_password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if input_password and confirm_password:
            if input_password != confirm_password:
                raise ValidationError("Passwords do not match")
        return confirm_password

    class Meta:
        model = Student
        fields = (
            "username",
            "first_name",
            "last_name",
            "email_address",
            "current_school",
            "borough",
            "input_password",
            "confirm_password",
        )
        exclude = ["password"]
        widgets = {
            "borough": forms.Select(
                choices=BOROUGH_CHOICES, attrs={"class": "custom-select mr-sm-2"}
            )
        }
        labels = {
            "input_password": _("Password"),
            "confirm_password": _("Password (once more please)"),
        }


class AdminStaffRegisterForm(ModelForm):
    input_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Admin_Staff.objects.filter(username=username).exists():
            raise ValidationError("Username already in use")
        return username

    def clean_supervisor_email(self):
        supervisor_email = self.cleaned_data["supervisor_email"]
        email = self.cleaned_data["email_address"]
        if supervisor_email and email:
            if supervisor_email == email:
                raise ValidationError("Supervisor email can not be the same as yours")
        return supervisor_email

    def clean_input_password(self):
        input_password = self.cleaned_data["input_password"]
        pattern = re.compile(REG_EX)
        if re.search(pattern, input_password):
            return input_password
        else:
            raise ValidationError(
                "The password should be minimum 8 characters long and should contain "
                "at least 1 of each\nUppercase, Lowercase, 1digit, 1 symbol(@#$%^&+=_-)"
            )

    def clean_confirm_password(self):
        if "input_password" not in self.cleaned_data:
            return ValidationError("Password not valid")
        input_password = self.cleaned_data["input_password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if input_password and confirm_password:
            if input_password != confirm_password:
                raise ValidationError("Passwords do not match")
        return confirm_password

    class Meta:
        model = Admin_Staff
        fields = (
            "username",
            "first_name",
            "last_name",
            "email_address",
            "school",
            "supervisor_email",
            "input_password",
            "confirm_password",
        )
        exclude = ["password"]
        labels = {
            "supervisor_email": _("Supervisor's Email"),
            "input_password": _("Password"),
            "confirm_password": _("Password (once more please)"),
        }
