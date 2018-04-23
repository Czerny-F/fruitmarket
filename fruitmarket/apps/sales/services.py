from typing import Iterator, Dict, Any
from django.utils.functional import cached_property
from fruitmarket.apps.products.models import Fruit
from .managers import FruitSalesQuerySet


class FruitSalesStats(object):

    def __init__(self, queryset: FruitSalesQuerySet):
        self._queryset = queryset

    @cached_property
    def queryset(self) -> FruitSalesQuerySet:
        return self._queryset.select_related()

    @cached_property
    def total(self) -> int:
        return self.queryset.total()

    @cached_property
    def fruits(self):
        return Fruit.objects.filter(fruitsales__in=self.queryset).distinct()

    def breakdown(self) -> Iterator[Dict[str, Any]]:
        for fruit in self.fruits:
            sales = [obj for obj in self.queryset if obj.fruit == fruit]
            yield {
                'fruit': fruit,
                'amount': sum(s.amount for s in sales),
                'quantity': sum(s.quantity for s in sales),
            }
