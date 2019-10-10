from django.forms import ModelForm
from register.models import User
from django import forms


class LoginForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field, 'required': True})

    class Meta:
        model = User
        fields = ['username', 'password']