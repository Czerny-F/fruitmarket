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
            file_.readline().decode(ENCODING)
        except UnicodeDecodeError:
            raise forms.ValidationError(_("invalid encoding"))
        else:
            file_.seek(0)
            reader = csv.reader(codecs.iterdecode(file_, ENCODING))
            self.cleaned_data['reader'] = reader

        return file_

    def save(self):
        assert 'reader' in self.cleaned_data

        for row in self.cleaned_data['reader']:
            print(row)
