from django.db import models


class FruitSalesManager(models.Manager):

    def total(self) -> int:
        return sum([obj.amount for obj in self.only('amount')])
