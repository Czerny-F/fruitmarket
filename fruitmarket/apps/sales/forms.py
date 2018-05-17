from django import forms


class FruitSalesCSVUploadForm(forms.Form):
    file_ = forms.FileField()
