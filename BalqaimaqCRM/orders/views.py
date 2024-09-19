import datetime
from django.shortcuts import render, get_object_or_404, redirect, resolve_url, HttpResponse
from django.http import JsonResponse

from .models import Order, OrderItem
from clients.models import Client
from storage.models import Product
from .forms import OrderCreateForm, OrderUpdateForm, OrderItemAddForm

def orders_list_view(request):
    # TODO доработать работу с датами
    date = request.GET.get("date", "today")
    if date == "today": 
        start = datetime.date.today()
        end = start + datetime.timedelta(days=1)
    elif date == "yesterday":
        start = datetime.date.today() - datetime.timedelta(days=1)
        end = datetime.date.today()
    elif date == "week":
        start = datetime.date.today() - datetime.timedelta(days=7)
        end = datetime.date.today() + datetime.timedelta(days=1)
    elif date == "month":
        start = datetime.date.today() - datetime.timedelta(days=30)
        end = datetime.date.today() + datetime.timedelta(days=1)
    orders_stage1 = Order.objects.filter(stage=1).filter(created_at__gt=start).filter(created_at__lt=end)
    orders_stage2 = Order.objects.filter(stage=2).filter(created_at__gt=start).filter(created_at__lt=end)
    orders_stage3 = Order.objects.filter(stage=3).filter(created_at__gt=start).filter(created_at__lt=end)
    orders_stage4 = Order.objects.filter(stage=4).filter(created_at__gt=start).filter(created_at__lt=end)
    orders_stage1_price = sum(order.get_total_cost() for order in orders_stage1)
    orders_stage2_price = sum(order.get_total_cost() for order in orders_stage2)
    orders_stage3_price = sum(order.get_total_cost() for order in orders_stage3)
    orders_stage4_price = sum(order.get_total_cost() for order in orders_stage4)
    return render(request, "orders/orders_list.html", {
        "section": "orders",
        "orders_stage1": orders_stage1,
        "orders_stage2": orders_stage2,
        "orders_stage3": orders_stage3,
        "orders_stage4": orders_stage4,
        "orders_stage1_price": orders_stage1_price,
        "orders_stage2_price": orders_stage2_price,
        "orders_stage3_price": orders_stage3_price,
        "orders_stage4_price": orders_stage4_price,
	})
    
def orders_create_view(request, phone_number):
    if request.method == "POST":
        form = OrderCreateForm(data=request.POST)
        if form.is_valid():
            order = form.save()
            url = resolve_url("orders_detail", order.id)
            return redirect(url)
    client = Client.objects.get(phone_number=phone_number)
    form = OrderCreateForm(instance=client)
    
    return render(request, "orders/orders_create.html", {
        "section": "orders",
        "form": form
    })
    
def orders_update_view(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        form = OrderUpdateForm(data=request.POST,
                               instance=order)
        if form.is_valid():
            form.save()
            return redirect("orders_detail", order.id)
    else:
        form = OrderUpdateForm(instance=order)
        
    return render(request, "orders/orders_create.html", {
        "section": "orders",
        "form": form
    })
    
def orders_detail_view(request, order_id):
    error = False
    if request.method == "POST":
        form = OrderItemAddForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            
            # if order has this item
            order_items = OrderItem.objects.filter(order_id=order_id)
            for order_item in order_items:
                if form.product_id == order_item.product_id:
                    order_item.amount += form.amount
                    order_item.save()
                    url = resolve_url("orders_detail", order_id)
                    return redirect(url)
                    
            product = Product.objects.get(id=form.product_id)
            product.amount -= form.amount
            if product.amount >= 0:
                form.order_id = order_id 
                form.save()
                product.save()
                url = resolve_url("orders_detail", order_id)
                return redirect(url)
            else:
                error = True
        
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order_id=order_id)
    form = OrderItemAddForm()
    
    return render(request, "orders/orders_detail.html", {
        "section": "orders",
        "order": order,
        "order_items": order_items,
        "form": form,
        "error": error
    })
    
def orders_delete_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        items = OrderItem.objects.filter(order_id=order.id)
        for item in items:
            product = Product.objects.get(id=item.product_id)
            product.amount += item.amount
            product.save()
        order.delete()
        return redirect('orders_list')
    return render(request, "orders/orders_delete.html", {
        'section': "orders",
        "order": order,
    })
    
def orders_item_delete_view(request, item_id):
    order_item = OrderItem.objects.get(id=item_id)
    order_id = order_item.order_id
    if request.method == "POST":
        order_item.delete()
        return redirect("orders_detail", order_id)
    return render(request, "orders/orders_delete.html", {
        "section": "orders",
        "order": order_item 
    })
    
def orders_column_update_view(request, order_id, order_stage):
    if request.method == "GET":
        order = Order.objects.get(id=order_id)
        order.stage = order_stage[-1]
        order.save()
        return JsonResponse({"saved": "OK"})
    