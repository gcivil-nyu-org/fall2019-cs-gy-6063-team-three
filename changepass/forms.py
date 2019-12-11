from django.forms import ModelForm
from register.models import User, Student, Admin_Staff
from django import forms
from django.forms import ValidationError
import re

REG_EX = (
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&_-]{8,20}$"
)  # noqa: W605, E501


class changepassForm(ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field, "required": True}
            )

    def clean_new_password(self):
        new_password = self.cleaned_data["new_password"]
        pattern = re.compile(REG_EX)
        if re.search(pattern, new_password):
            return new_password
        else:
            raise ValidationError("Password requirements don't match")

    def clean_confirm_password(self):
        if "new_password" not in self.cleaned_data:
            return ValidationError("Password not valid")
        new_password = self.cleaned_data["new_password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError("New passwords do not match")
        return confirm_password

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        return old_password

    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_password"]


class resetPassFormStudent(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field, "required": True}
            )

    def clean_email_address(self):
        email = self.cleaned_data["email_address"]
        if not Student.objects.filter(email_address=email).exists():
            raise ValidationError("There is no account with this email address!")
        return email

    class Meta:
        model = Student
        fields = ["email_address"]


class resetPassFormAdmin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field, "required": True}
            )

    def clean_email_address(self):
        email = self.cleaned_data["email_address"]
        if not Admin_Staff.objects.filter(email_address=email).exists():
            raise ValidationError("There is no account with this email address!")
        return email

    class Meta:
        model = Admin_Staff
        fields = ["email_address"]
