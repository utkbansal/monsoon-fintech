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

    # TODO: Can take care of an invalid form

    def form_valid(self, form):
        pdf = form.save()

        # Generate and save CSV file
        converter = PDFToCSVConverter(pdf.file.path)
        self.save_file_contents(converter.cleaned_data)
        output = StringIO()
        converter.write(output)
        output.seek(0)
        name = str(uuid.uuid4()) + '.csv'
        pdf.csv.save(name, ContentFile(output.read()))
        pdf.save()

        # Perform the search

        # NOTE: have done .first() on the next 2 queries because there can be duplicate data
        year = Year.objects.filter(value=form.cleaned_data['query_year']).first()
        data = Data.objects.filter(year=year, variable__exact=form.cleaned_data['query_variable']).first()

        if year is None or data is None:
            response = "Value not found"
        else:
            response = "Value of " + form.cleaned_data['query_variable'] + " is " + data.amount

        return render(self.request, 'result.html', context={'download': pdf.csv.url, 'value': response})

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

        Data.objects.bulk_create(data_objects)
