from django import forms

from .models import Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'phone_number', 'address', 'type_of_payment', 'type_of_order'
        
class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'phone_number', 'address', 'type_of_payment', 'type_of_order', "stage", "review"
        
class OrderItemAddForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = 'product', 'amount'
        
class OrderSortForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "stage", 
