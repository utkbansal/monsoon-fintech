from __future__ import unicode_literals

import uuid
from StringIO import StringIO

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.generic import FormView

from .forms import UploadForm
from .models import Year, Data
from .parser import PDFToCSVConverter


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
        self.save_file_contents(converter.cleaned_data)
        output = StringIO()
        converter.write(output)
        output.seek(0)
        name = str(uuid.uuid4()) + '.csv'
        pdf.csv.save(name, ContentFile(output.read()))
        pdf.save()
        return render(self.request, 'result.html', context={'download': pdf.csv.url})

    def save_file_contents(self, data):
        """
        Save parsed data to db
        :param data: list of lists
        :return: None
        """

        print("complete data is ", data)

        year_2015, created = Year.objects.get_or_create(value='2015')
        year_2016, created = Year.objects.get_or_create(value='2016')

        data_objects = []

        for value in data:
            print(value)
            data_objects.append(Data(amount=value[1], year=year_2015, variable=value[0]))
            data_objects.append(Data(amount=value[2], year=year_2016, variable=value[0]))

        # print(data_objects)

        Data.objects.bulk_create(data_objects)
