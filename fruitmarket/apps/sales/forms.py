import csv
import codecs
from django import forms
from django.utils.translation import ugettext_lazy as _

ENCODING = 'utf-8'


class FruitSalesCSVUploadForm(forms.Form):
    file_ = forms.FileField()

    def clean_file_(self):
        file_ = self.cleaned_data['file_']
        if file_.content_type != 'text/csv':
            raise forms.ValidationError(_("invalid file"))

        try:
            file_.read().decode(ENCODING)
        except UnicodeDecodeError:
            raise forms.ValidationError(_("invalid encoding"))
        else:
            file_.seek(0)

        return file_

    def save(self):
        file_ = self.cleaned_data['file_']
        for row in csv.reader(codecs.iterdecode(file_, ENCODING)):
            print(row)
