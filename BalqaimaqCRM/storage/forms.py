from django import forms

from .models import Product, Supply, Combo, ProductsInCombo


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "amount", "sell_price", "cost_price", "description", "image"
        
class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = "product", "worker", "amount"
        
class ComboForm(forms.ModelForm):
    class Meta:
        model = Combo
        fields = "name", "price", "discount", "description", "image"
        
class AddProductToComboForm(forms.ModelForm):
    class Meta:
        model = ProductsInCombo
        fields = "product", "amount", 'combo'
        widgets = {'combo': forms.HiddenInput()}