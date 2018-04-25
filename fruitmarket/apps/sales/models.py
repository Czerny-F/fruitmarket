from typing import List
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from fruitmarket.core.models import EditableModel
from fruitmarket.apps.products.models import Fruit
from .managers import FruitSalesManager


class FruitSales(EditableModel):
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(_("quantity"))
    amount = models.PositiveIntegerField(_("amount"), editable=False)
    sold_at = models.DateTimeField(_("datetime sold"), default=timezone.now,
                                   db_index=True)

    objects = FruitSalesManager()

    class Meta:
        verbose_name = _("sale of fruit")
        verbose_name_plural = _("sales of fruit")
        ordering = ['-sold_at']

    def __str__(self):
        return _("%(fruit)s sold at %(sold_at)s") % {
            'fruit': self.fruit,
            'sold_at': self.sold_at_astz.strftime('%F %R'),
        }

    @property
    def sold_at_astz(self):
        tz = timezone.get_current_timezone()
        return self.sold_at.astimezone(tz)

    @classmethod
    def gross(cls) -> int:
        return cls.objects.gross()


@receiver(pre_save, sender=FruitSales)
def calculate_amount(sender, instance, **kwargs):
    if not instance.pk:
        instance.amount = instance.fruit.unit_price * instance.quantity


class FruitSalesSet(object):

    def __init__(self, fruit: Fruit, sales: List[FruitSales]):
        self.fruit = fruit
        self.sales = sales

    @property
    def total_amount(self) -> int:
        return sum(s.amount for s in self.sales)

    @property
    def total_quantity(self) -> int:
        return sum(s.quantity for s in self.sales)
