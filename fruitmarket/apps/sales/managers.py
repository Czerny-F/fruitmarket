import datetime
from django_pandas.managers import DataFrameQuerySet, DataFrameManager
from fruitmarket.core.utils import to_datetime, get_current_month, get_next_month


class BaseSalesQuerySetMixin(object):
    date_field = None

    def _periodic_filter(self, since: datetime.date, until: datetime.date):
        return self.filter(**{
            '%s__gte' % self.date_field: to_datetime(since),
            '%s__lt' % self.date_field: to_datetime(until),
        })

    def daily(self, date: datetime.date):
        return self._periodic_filter(date, date + datetime.timedelta(days=1))

    def monthly(self, date: datetime.date):
        return self._periodic_filter(get_current_month(date), get_next_month(date))

    def total_amount(self) -> int:
        return sum(obj.amount for obj in self)


class BaseSalesManager(DataFrameManager):

    def gross(self) -> int:
        return self.get_queryset().total_amount()


class FruitSalesQuerySet(BaseSalesQuerySetMixin, DataFrameQuerySet):
    date_field = 'sold_at'


FruitSalesManager = BaseSalesManager.from_queryset(FruitSalesQuerySet)
