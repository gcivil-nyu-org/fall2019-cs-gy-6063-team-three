from django.forms import ValidationError
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
import re
from .models import User

BOROUGH_CHOICES = [('', 'Borough'), ('MN', 'Manhattan'), ('BK', 'Brooklyn'), ('QN', 'Queens'), ('BX', 'The Bronx'),
                   ('SI', 'Staten Island')]


class RegisterForm(ModelForm):
    input_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field})

        self.fields['confirm_password'].widget.attrs.update({'placeholder': 'Password (Once more)'})

    def clean_input_password(self):
        input_password = self.cleaned_data['input_password']
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        pattern = re.compile(reg)
        if re.search(pattern,input_password):
            return input_password
        else:
            raise ValidationError('The password should be minimum 8 characters long and should contain at least 1 of each\n'
                                  'Uppercase, Lowercase, 1digit, 1 symbol(@#$%^&+=_-)')

    def clean_confirm_password(self):
        if 'input_password' not in self.cleaned_data:
            return ValidationError("Password not valid")
        input_password = self.cleaned_data['input_password']
        confirm_password = self.cleaned_data['confirm_password']
        if input_password and confirm_password:
            if input_password != confirm_password:
                raise ValidationError("Passwords do not match")
        return confirm_password

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email_address', 'current_school', 'borough',
                  'input_password', 'confirm_password')
        exclude = ['password']
        widgets = {
            'borough': forms.Select(choices=BOROUGH_CHOICES, attrs={'class': 'custom-select mr-sm-2'})
        }
        labels = {
            'input_password': _('Password'),
            'confirm_password': _('Password (once more please)')
        }
        help_texts = {
            # 'username': _('A username you can easily remember (can be same as your email address)'),
            # 'first_name': _('Legal first name (same as on your state issued ID) - John'),
            # 'last_name': _('Legal last name (same as on your state issued ID) - Doe or M. Doe '),
            # 'email_address': _('An active email address that you will receive notifications on'),
            # 'current_school': _('Current school you are enrolled with'),
            # 'borough': _('MN (Manhattan), BK (Brooklyn), QN (Queens), BX (The Bronx), SI (Staten Island)'),
        }
