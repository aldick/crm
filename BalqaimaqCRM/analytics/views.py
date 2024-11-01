import datetime
from calendar import monthrange
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from orders.models import Order, OrderItem
from storage.models import Product


def selling_view(request):
    return render(request, "analytics/selling.html", {
		"section": "analytics"
	})

def _get_orders(date):
    start = None
    end = None
    days = None
    if date[1] == "w":
        days = 7
        if date == 'cw':
            start = datetime.date.today() - datetime.timedelta(datetime.date.today().weekday())
        elif date == "pw":
            start = datetime.date.today() - datetime.timedelta(datetime.date.today().weekday()) - datetime.timedelta(7)
    elif date[1] == 'm':
        current_year = datetime.date.today().year
        if date == 'cm':
            month = datetime.date.today().month
            days = monthrange(current_year, month)[1]
            start = datetime.date.today() - datetime.timedelta(datetime.date.today().day) + datetime.timedelta(1)
        elif date == "pm":
            month = datetime.date.today().month - 1
            days = monthrange(current_year, month)[1]
            start = datetime.date.today() - datetime.timedelta(datetime.date.today().day) - datetime.timedelta(days) + datetime.timedelta(1)
    end = start + datetime.timedelta(days)
            
    orders = Order.objects.filter(created_at__gt=start).filter(created_at__lt=end)
    return orders, days, start, end
    
def get_selling(request, date):
    orders_dict = {'days': {}}
    orders, days, start, end = _get_orders(date)
    total_sum = 0
    
    for i in range(1, days+1):
        orders_dict["days"][i] = 0
        
    if date[1] == 'w':         
        for order in orders:
        	total_sum += order.get_total_cost()
        	orders_dict["days"][order.created_at.weekday()] += order.get_total_cost()
    elif date[1] == 'm':
        for order in orders:
            total_sum += order.get_total_cost()
            orders_dict["days"][order.created_at.day] = order.get_total_cost()
         
    orders_dict["total_sum"] = total_sum
         
    return JsonResponse(orders_dict)
    
def products_view(request):
    return render(request, "analytics/products.html", {
        "section": "analytics"
    })
    
def get_products(request, date):
    products_list = {}
    orders, days, start, end = _get_orders(date)
    
    products = Product.objects.all()
    for product in products:
        products_list[product.name] = 0
    
    order_items = OrderItem.objects.all()
    for item in order_items:
        if item.order.created_at.date() >= start and item.order.created_at.date() < end:
            products_list[item.product.name] += item.amount
            print(item.order)
    
    return JsonResponse(products_list)