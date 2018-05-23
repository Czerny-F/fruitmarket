import datetime
from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
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
        messages.success(self.request, form.result)
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
    fields = ['fruit', 'quantity', 'sold_at']


@method_decorator(login_required, name='dispatch')
class FruitSalesUpdate(FruitSalesEditMixin, generic.UpdateView):
    fields = ['fruit', 'quantity', 'sold_at']


@method_decorator(login_required, name='dispatch')
class FruitSalesDelete(FruitSalesEditMixin, generic.DeleteView):
    pass


@method_decorator(login_required, name='dispatch')
class FruitSalesStatsOverview(generic.dates.MonthMixin,
                              generic.dates.DayMixin,
                              generic.dates.DateMixin,
                              generic.ListView):
    model = FruitSales
    stats_class = FruitSalesStats
    date_field = 'sold_at'
    allow_empty = True
    template_name = 'sales/fruitsales_stats.html'

    def get_context_data(self, **kwargs):
        date = datetime.date.today()
        kwargs.update({
            'gross': self.model.objects.gross(),
            'monthly': self.get_monthly_stats(date),
            'daily': self.get_daily_stats(date),
        })
        return super().get_context_data(**kwargs)

    def get_monthly_stats(self, date, months=3):
        for _ in range(months):
            yield {
                'date': self._get_current_month(date),
                'stats': self.stats_class(self.model.objects.monthly(date)),
            }
            date = self.get_previous_month(date)

    def get_daily_stats(self, date, days=3):
        for _ in range(days):
            yield {
                'date': date,
                'stats': self.stats_class(self.model.objects.daily(date)),
            }
            date = self.get_previous_day(date)
