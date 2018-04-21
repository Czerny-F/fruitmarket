from django.contrib import admin
from .models import FruitSales


@admin.register(FruitSales)
class FruitSalesAdmin(admin.ModelAdmin):
    readonly_fields = ('amount', 'updated_at', 'created_at')
    list_display = ('fruit', 'quantity', 'amount', 'sold_at')
