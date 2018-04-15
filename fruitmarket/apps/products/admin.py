from django.contrib import admin
from .models import Fruit


@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    readonly_fields = ('updated_at', 'created_at')
    list_display = ('name', 'unit_price', 'updated_at', 'created_at')
