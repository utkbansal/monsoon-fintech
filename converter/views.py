from __future__ import unicode_literals

from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from .forms import UploadForm


class UploadView(FormView):
    form_class = UploadForm
    template_name = 'upload.html'
    success_url = '/result/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        print('valid form')
        return redirect(self.success_url)

    def form_invalid(self, form):
        print form.errors


class ResultView(TemplateView):
    template_name = 'result.html'
