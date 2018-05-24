from django.urls import path, include
from . import views

app_name = 'sales'
urlpatterns = [
    path('fruits/', include(([
        path('', views.FruitSalesList.as_view(), name='list'),
        path('add/', views.FruitSalesCreate.as_view(), name='add'),
        path('<int:pk>/', include([
            path('', views.FruitSalesUpdate.as_view(), name='edit'),
            path('delete/', views.FruitSalesDelete.as_view(), name='delete'),
        ])),
    ], 'fruits'))),
    path('stats/', include(([
        path('', views.FruitSalesStatsOverview.as_view(), name='overview'),
        path('pandas/', views.FruitSalesPandasStats.as_view(), name='pandas'),
    ], 'stats'))),
]
