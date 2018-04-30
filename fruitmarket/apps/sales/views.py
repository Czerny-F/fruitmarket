from django.views import generic
from .models import FruitSales


class FruitSalesStatsOverview(generic.TemplateView):
    template_name = 'sales/stats.html'

    def get_context_data(self, **kwargs):
        kwargs['gross'] = FruitSales.objects.gross()
        return super().get_context_data(**kwargs)
