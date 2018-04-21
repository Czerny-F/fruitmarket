from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SalesConfig(AppConfig):
    name = 'fruitmarket.apps.sales'
    label = 'sales'
    verbose_name = _("sales")
