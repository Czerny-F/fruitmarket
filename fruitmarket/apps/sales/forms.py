import csv
import codecs
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from fruitmarket.apps.products.models import Fruit
from .models import FruitSales


class BaseCSVUploadForm(forms.Form):
    file_ = forms.FileField()
    csv_form_class = None

    def clean_file_(self):
        file_ = self.cleaned_data['file_']
        if file_.content_type != 'text/csv':
            raise forms.ValidationError(_("invalid file."))

        try:
            file_.read().decode(settings.FILE_CHARSET)
        except UnicodeDecodeError:
            raise forms.ValidationError(_("invalid encoding."))
        else:
            file_.seek(0)

        return file_

    @property
    def imported(self) -> list:
        assert hasattr(self, '_imported'), 'You must call `.save()` first.'
        return self._imported

    @property
    def ignored(self) -> list:
        assert hasattr(self, '_ignored'), 'You must call `.save()` first.'
        return self._ignored

    @property
    def result(self) -> str:
        assert hasattr(self, '_imported') and hasattr(self, '_ignored'), (
            'You must call `.save()` first.'
        )
        return _("%(imported_num)d line(s) imported,"
                 " %(ignored_num)d line(s) ignored(%(ignored_line)s).") % {
                     'imported_num': len(self.imported),
                     'ignored_num': len(self.ignored),
                     'ignored_line': ','.join(str(ign['line']) for ign in self.ignored),
                 }

    def save(self):
        assert hasattr(self, 'cleaned_data'), (
            'You must call `.is_valid()` first.'
        )

        assert not self.errors, (
            'You cannot call `.save()` with invalid data.'
        )

        file_ = self.cleaned_data['file_']
        reader = csv.DictReader(codecs.iterdecode(file_, settings.FILE_CHARSET),
                                fieldnames=self.csv_fields())
        self._imported = []
        self._ignored = []
        for i, row in enumerate(reader):
            form = self.get_csv_form(row)
            if form.is_valid():
                self._imported.append(form.save())
            else:
                self._ignored.append({'line': i + 1,
                                      'row': list(row.values()),
                                      'errors': form.errors})

    def get_csv_form(self, *args, **kwargs) -> forms.BaseForm:
        assert issubclass(self.csv_form_class, forms.BaseForm), 'Specify csv_form_class.'
        return self.csv_form_class(*args, **kwargs)

    def csv_fields(self) -> list:
        form = self.get_csv_form()
        return list(form.fields.keys())


class FruitSalesCSVForm(forms.ModelForm):
    fruit = forms.ModelChoiceField(queryset=Fruit.objects.all(), to_field_name='name')

    class Meta:
        model = FruitSales
        fields = '__all__'


class FruitSalesCSVUploadForm(BaseCSVUploadForm):
    csv_form_class = FruitSalesCSVForm
