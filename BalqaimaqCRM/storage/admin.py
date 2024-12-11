from django.contrib import admin
from .models import Product, Combo, ProductsInCombo

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Combo)
class ComboAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductsInCombo)
class ProductsInComboAdmin(admin.ModelAdmin):
    pass