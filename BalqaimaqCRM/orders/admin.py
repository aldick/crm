from django.contrib import admin
from .models import Order, OrderComboItem

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderComboItem)
class OrderComboItemAdmin(admin.ModelAdmin):
    pass