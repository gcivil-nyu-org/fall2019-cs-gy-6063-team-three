from django import forms


class SaveHighSchoolsForm(forms.Form):
    limit = forms.IntegerField(min_value=1)
