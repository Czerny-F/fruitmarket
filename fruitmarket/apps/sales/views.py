from django.views import generic
from django.urls import reverse_lazy
from .models import FruitSales
from .services import FruitSalesStats


class FruitSalesList(generic.ListView):
    model = FruitSales
    queryset = FruitSales.objects.select_related()


class FruitSalesUpdate(generic.UpdateView):
    model = FruitSales
    fields = '__all__'
    success_url = reverse_lazy('sales:fruits:list')


class FruitSalesStatsOverview(generic.TodayArchiveView):
    queryset = FruitSales.objects.all()
    date_field = 'sold_at'
    allow_empty = True
    template_name = 'sales/stats.html'

    def get_context_data(self, **kwargs):
        date = kwargs['day']
        kwargs.update({
            'gross': FruitSales.objects.gross(),
            'monthly': self.get_monthly_stats(date),
            'daily': self.get_daily_stats(date),
        })
        return super().get_context_data(**kwargs)

    def get_monthly_stats(self, date):
        for lookup in self._make_monthly_lookups(date):
            yield {
                'date': lookup['date'],
                'stats': FruitSalesStats(self.get_dated_queryset(**lookup['kwargs'])),
            }

    def _make_monthly_lookups(self, date, months=3):
        for _ in range(months):
            yield {
                'date': self._get_current_month(date),
                'kwargs': self._make_single_month_lookup(date),
            }
            date = self.get_previous_month(date)

    def _make_single_month_lookup(self, date) -> dict:
        date_field = self.get_date_field()
        since = self._make_date_lookup_arg(self._get_current_month(date))
        until = self._make_date_lookup_arg(self._get_next_month(date))
        return {
            '%s__gte' % date_field: since,
            '%s__lt' % date_field: until,
        }

    def get_daily_stats(self, date):
        for lookup in self._make_daily_lookups(date):
            yield {
                'date': lookup['date'],
                'stats': FruitSalesStats(self.get_dated_queryset(**lookup['kwargs'])),
            }

    def _make_daily_lookups(self, date, days=3):
        for _ in range(days):
            yield {
                'date': date,
                'kwargs': self._make_single_date_lookup(date),
            }
            date = self.get_previous_day(date)
