from django.urls import path, include
from . import views

app_name = 'sales'
urlpatterns = [
    path('stats/', include(([
        path('', views.FruitSalesStats.as_view(), name='overview'),
    ], 'stats'))),
]
