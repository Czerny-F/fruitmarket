from typing import List, Iterator
from django.utils.functional import cached_property
from fruitmarket.apps.products.models import Fruit
from .managers import FruitSalesQuerySet
from .models import FruitSales


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

    def breakdown(self) -> Iterator[FruitSalesSet]:
        for fruit in self.fruits:
            sales = [obj for obj in self.queryset if obj.fruit == fruit]
            yield FruitSalesSet(fruit, sales)
