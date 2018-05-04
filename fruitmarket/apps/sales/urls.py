from django.urls import path, include
from . import views

app_name = 'sales'
urlpatterns = [
    path('fruits/', include(([
        path('', views.FruitSalesList.as_view(), name='list'),
    ], 'fruits'))),
    path('stats/', include(([
        path('', views.FruitSalesStatsOverview.as_view(), name='overview'),
    ], 'stats'))),
]
