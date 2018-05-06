from django.urls import path, include
from . import views

app_name = 'products'
urlpatterns = [
    path('fruits/', include(([
        path('', views.FruitList.as_view(), name='list'),
        path('add/', views.FruitCreate.as_view(), name='add'),
        path('<int:pk>/', include([
            path('', views.FruitUpdate.as_view(), name='edit'),
            path('delete/', views.FruitDelete.as_view(), name='delete'),
        ])),
    ], 'fruits'))),
]
