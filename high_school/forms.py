from django import forms


class SaveHighSchoolsForm(forms.Form):
    limit = forms.IntegerField()
