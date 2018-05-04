from django.urls import path, include
from . import views

app_name = 'products'
urlpatterns = [
    path('fruits/', include(([
        path('', views.FruitList.as_view(), name='list'),
        path('<int:pk>/', views.FruitUpdate.as_view(), name='edit'),
    ], 'fruits'))),
]
