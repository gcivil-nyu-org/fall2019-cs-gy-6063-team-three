from django.forms import ModelForm
from register.models import User
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
                {"class": "form-control", "placeholder": "", "required": True}
            )

    def clean_new_password(self):
        new_password = self.cleaned_data["new_password"]
        pattern = re.compile(REG_EX)
        if re.search(pattern, new_password):
            return new_password
        else:
            raise ValidationError(
                "The password should be minimum 8 characters long and should contain at "
                "least 1 of each Uppercase, Lowercase, 1digit, 1 symbol(@#$%^&+=_-)"
            )

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
