from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import FruitSales
from .services import FruitSalesStats
from .forms import FruitSalesCSVUploadForm


class FruitSalesEditMixin(object):
    model = FruitSales
    success_url = reverse_lazy('sales:fruits:list')


@method_decorator(login_required, name='dispatch')
class FruitSalesList(FruitSalesEditMixin, generic.edit.FormMixin, generic.ListView):
    form_class = FruitSalesCSVUploadForm
    queryset = FruitSales.objects.select_related()

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object_list = self.get_queryset()
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class FruitSalesCreate(FruitSalesEditMixin, generic.CreateView):
    fields = '__all__'


@method_decorator(login_required, name='dispatch')
class FruitSalesUpdate(FruitSalesEditMixin, generic.UpdateView):
    fields = '__all__'


@method_decorator(login_required, name='dispatch')
class FruitSalesDelete(FruitSalesEditMixin, generic.DeleteView):
    pass


@method_decorator(login_required, name='dispatch')
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
