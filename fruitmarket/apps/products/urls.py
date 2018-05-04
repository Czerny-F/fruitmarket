from django.urls import path, include
from . import views

app_name = 'products'
urlpatterns = [
    path('fruits/', include(([
        path('', views.FruitList.as_view(), name='list'),
    ], 'fruits'))),
]
