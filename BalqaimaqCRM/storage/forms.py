from django import forms

from .models import Product, Supply


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "amount", "sell_price", "cost_price", "description", "image"
        
class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = "product", "worker", "amount"