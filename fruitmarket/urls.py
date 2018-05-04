from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('products/', include('fruitmarket.apps.products.urls')),
    path('sales/', include('fruitmarket.apps.sales.urls')),
    path('admin/', admin.site.urls),
]
