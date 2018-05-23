from typing import Iterator
from django.utils.functional import cached_property
from .managers import FruitSalesQuerySet


class FruitSalesSet(object):

    def __init__(self, fruit, sales: list):
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
    def fruits(self) -> set:
        return set(obj.fruit for obj in self.queryset)

    def total_amount(self) -> int:
        return self.queryset.total_amount()

    def breakdown(self) -> Iterator[FruitSalesSet]:
        for fruit in self.fruits:
            sales = list(obj for obj in self.queryset if obj.fruit == fruit)
            yield FruitSalesSet(fruit, sales)
