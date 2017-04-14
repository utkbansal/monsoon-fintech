from django import forms

from .models import PDF


class UploadForm(forms.ModelForm):
    query_variable = forms.CharField()
    query_year = forms.CharField()

    class Meta:
        model = PDF
        fields = ('file',)
