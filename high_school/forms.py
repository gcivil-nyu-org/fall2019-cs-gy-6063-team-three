from django import forms


class SaveHighSchools(forms.Form):
    limit = forms.IntegerField()
