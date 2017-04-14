from __future__ import unicode_literals

import uuid
from StringIO import StringIO

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.generic import FormView, TemplateView

from part1.parse import PDFToCSVConverter
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
            return self.form_invalid(form)

    def form_valid(self, form):
        pdf = form.save()
        converter = PDFToCSVConverter(pdf.file.path)
        output = StringIO()
        converter.write(output)
        output.seek(0)
        name = str(uuid.uuid4()) + '.csv'
        pdf.csv.save(name, ContentFile(output.read()))
        pdf.save()
        return render(self.request, 'result.html', context={'download': pdf.csv.url})


class ResultView(TemplateView):
    template_name = 'result.html'
