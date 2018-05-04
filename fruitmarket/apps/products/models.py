from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from fruitmarket.core.models import EditableModel


class Fruit(EditableModel):
    name = models.CharField(_("name"), max_length=256, unique=True)
    unit_price = models.PositiveIntegerField(_("unit price"))

    class Meta:
        verbose_name = _("fruit")
        verbose_name_plural = _("fruits")
        ordering = ['-updated_at', '-created_at']
        indexes = [
            models.Index(fields=['updated_at', 'created_at'],
                         name='products_fruit_timestamp_idx'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:fruits:edit', args=(self.pk,))
