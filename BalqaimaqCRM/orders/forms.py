from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'phone_number', 'address', 'type_of_payment', 'type_of_order'
