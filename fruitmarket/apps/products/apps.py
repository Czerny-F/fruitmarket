from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProductsConfig(AppConfig):
    name = 'fruitmarket.apps.products'
    label = 'products'
    verbose_name = _("products")
