from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from fruitmarket.core.models import EditableModel
from fruitmarket.apps.products.models import Fruit
from .managers import FruitSalesManager


class FruitSales(EditableModel):
    """
    果物販売情報モデル

    販売日時にindexあり
    売り上げはフォーム登録時、自動計算のためpre_saveシグナル利用
    カスタムマネージャ利用
    """
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(_("quantity"))
    amount = models.PositiveIntegerField(_("amount"))
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

    def get_absolute_url(self):
        return reverse('sales:fruits:edit', args=(self.pk,))

    @property
    def sold_at_astz(self):
        tz = timezone.get_current_timezone()
        return self.sold_at.astimezone(tz)


@receiver(pre_save, sender=FruitSales)
def calculate_amount(sender, instance, **kwargs):
    if not instance.pk and instance.amount is None:
        instance.amount = instance.fruit.unit_price * instance.quantity
