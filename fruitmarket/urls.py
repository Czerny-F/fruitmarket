from django.contrib import admin
from django.urls import path, include
from .core import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('products/', include('fruitmarket.apps.products.urls')),
    path('sales/', include('fruitmarket.apps.sales.urls')),
    path('admin/', admin.site.urls),
]
