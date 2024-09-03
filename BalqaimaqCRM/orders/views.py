from django.shortcuts import render, redirect, resolve_url

from .models import Order
from clients.models import Client
from .forms import OrderCreateForm

def orders_list_view(request):
    orders = Order.objects.all()
    return render(request, "orders/orders_list.html", {
        "section": "orders",
        "orders": orders
	})
    
