from django import forms


class UploadForm(forms.Form):
    query_variable = forms.CharField()
    query_year = forms.CharField()
    file = forms.FileField()
