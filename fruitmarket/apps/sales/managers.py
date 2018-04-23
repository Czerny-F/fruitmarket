from django.db import models


class FruitSalesQuerySet(models.QuerySet):

    def total(self) -> int:
        return sum(obj.amount for obj in self.only('amount'))


class FruitSalesManager(models.Manager):
    _queryset_class = FruitSalesQuerySet

    def gross(self) -> int:
        return self.get_queryset().total()
