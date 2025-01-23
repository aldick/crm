import datetime
from calendar import monthrange

from django.shortcuts import render, get_object_or_404, redirect, resolve_url, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem
from clients.models import Client
from storage.models import Product, Combo, ProductsInCombo
from orders.models import OrderComboItem
from .forms import OrderCreateForm, OrderUpdateForm, OrderItemAddForm, OrderComboAddForm
from analytics.views import _get_days

def _remove_samsa_from_storage(amount):
    samsa = Product.objects.get(name="Самса с говядиной")
    samsa.amount -= amount
    if samsa.amount < 0:
        error = True
    else:
        samsa.save()

def _add_samsa_gift(order, products_in_combo):
    if int(order.get_total_cost()) >= 15000 and "Самса в подарок 1 кг" not in products_in_combo and order.created_at.weekday() == 4:
        samsa_combo = Combo.objects.get(name="Самса в подарок 1 кг")
        gift = OrderComboItem(order_id=order.id, combo_id=samsa_combo.id, amount=1)
        gift.save()
        _remove_samsa_from_storage(amount=1)
    
    elif int(order.get_total_cost()) >= 10000 and "Самса в подарок 0.5 кг" not in products_in_combo and order.created_at.weekday() == 4:
        samsa_combo = Combo.objects.get(name="Самса в подарок 0.5 кг")
        gift = OrderComboItem(order_id=order.id, combo_id=samsa_combo.id, amount=1)
        gift.save()
        _remove_samsa_from_storage(amount=1)
            
    if int(order.get_total_cost()) < 10000 and "Самса в подарок 0.5 кг" in products_in_combo and order.created_at.weekday() == 4:
        samsa_combo = Combo.objects.get(name="Самса в подарок 0.5 кг")
        gift = OrderComboItem.objects.get(order_id=order.id, combo_id=samsa_combo.id)
        gift.delete()
        _remove_samsa_from_storage(amount=-1)
        
    if int(order.get_total_cost()) < 15000 and "Самса в подарок 1 кг" in products_in_combo and order.created_at.weekday() == 4:
        samsa_combo = Combo.objects.get(name="Самса в подарок 1 кг")
        gift = OrderComboItem.objects.get(order_id=order.id, combo_id=samsa_combo.id)
        gift.delete()
        _remove_samsa_from_storage(amount=-1)
        
def get_orders(request):
    date = request.GET.get("date", 't')
    start = None
    end = None
    days = None
    if date == "t" and request.GET.get("month", 'x') != 'x' :
        month = int(request.GET.get("month"))
        year = int(request.GET.get("year"))
        days = monthrange(year, month)[1]
        start = datetime.date(year, month, 1)
        end = start + datetime.timedelta(days)
    else:
        if date == "t": 
            days = 1
            start = datetime.date.today()
            end = start + datetime.timedelta(days=1)
        elif date == "y":
            days = 1
            start = datetime.date.today() - datetime.timedelta(days=1)
            end = datetime.date.today()
        elif date[1] == "w":
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
                month = datetime.date.today().month
                days = monthrange(current_year, month)[1]
                start = datetime.date.today() - datetime.timedelta(datetime.date.today().day) - datetime.timedelta(days) + datetime.timedelta(1)
        end = start + datetime.timedelta(days)
    
    orders_stage1 = Order.objects.filter(stage=1).filter(created_at__gt=start).filter(created_at__lt=end)
    orders_stage2 = Order.objects.filter(stage=2).filter(created_at__gt=start).filter(created_at__lt=end)
    orders_stage3 = Order.objects.filter(stage=3).filter(created_at__gt=start).filter(created_at__lt=end)
    orders_stage4 = Order.objects.filter(stage=4).filter(created_at__gt=start).filter(created_at__lt=end)
    orders_stage1_price = sum(order.get_total_cost() for order in orders_stage1)
    orders_stage2_price = sum(order.get_total_cost() for order in orders_stage2)
    orders_stage3_price = sum(order.get_total_cost() for order in orders_stage3)
    orders_stage4_price = sum(order.get_total_cost() for order in orders_stage4)
    
    orders = {1: {}, 2: {}, 3: {}, 4: {}}
    orders_stages = [orders_stage1, orders_stage2, orders_stage3, orders_stage4]
    for i in range(1, 5):
        for order in orders_stages[i-1]:
            orders[i][order.id] = {
                "id": order.id,
                'phone_number': order.phone_number.phone_number,
                'address': order.address,
                'date': order.created_at.strftime("%d.%m.%Y"),
                'time': order.created_at.strftime("%H:%M"),
                'total_cost': order.get_total_cost(),
                'url': {
                    "orders_detail_url": resolve_url("orders_detail", order.id),
                    "clients_detail_url": resolve_url("clients_detail", order.phone_number)
                }
            }
    return JsonResponse(orders)
            

@login_required        
def orders_list_view(request):
    return render(request, "orders/orders_list.html", {
        "section": "orders",
	})

@login_required
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
    
@login_required
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
    
@login_required
def orders_detail_view(request, order_id):
    error = False
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order_id=order_id)
    
    #need to calculate amount of products in each combo
    order_combos = OrderComboItem.objects.filter(order_id=order_id)
    products_in_combo = {}
    for order_combo in order_combos:
        temp = ProductsInCombo.objects.filter(combo=order_combo.combo.id)
        products_in_combo[order_combo.combo.name] = {}
        for product in temp:
            products_in_combo[order_combo.combo.name][product.product.name] = product.amount
    
    products_in_combo_with_amount = {}
    for order_combo in order_combos:
        temp = ProductsInCombo.objects.filter(combo=order_combo.combo.id)
        products_in_combo_with_amount[order_combo.combo.name] = {'amount': order_combo.amount}
        for product in temp:
            products_in_combo_with_amount[order_combo.combo.name][product.product.name] = product.amount
        
    _add_samsa_gift(order, products_in_combo)
        
    if request.method == "POST":
        order_item_add_form = OrderItemAddForm(request.POST)
        order_combo_add_form = OrderComboAddForm(request.POST)
        
        if order_item_add_form.is_valid():
            order_item_add_form = order_item_add_form.save(commit=False)
            
            product = Product.objects.get(id=order_item_add_form.product_id)
            product.amount -= order_item_add_form.amount
            
            if product.amount >= 0:
                order_items = OrderItem.objects.filter(order_id=order_id)
                
                product.save()
                    
                order = Order.objects.get(id=order_id)
                order.phone_number.total += order_item_add_form.product.sell_price * order_item_add_form.amount
                order.phone_number.save()
                
                product_in_order_flag = False  
                for order_item in order_items:
                    if order_item_add_form.product_id == order_item.product_id:
                        order_item.amount += order_item_add_form.amount
                        order_item.save()
                        product_in_order_flag = True
                
                if product_in_order_flag == False:
                    order_item_add_form.order_id = order_id
                    order_item_add_form.save()

                url = resolve_url("orders_detail", order_id)
                return redirect(url)
            
            else:
                error = True
                
        if order_combo_add_form.is_valid():
            order_combo_add_form = order_combo_add_form.save(commit=False)
            
            combo = Combo.objects.get(name=order_combo_add_form.combo.name)
            products = ProductsInCombo.objects.filter(combo=combo)
            for product in products:
                if product.product.amount - product.amount * order_combo_add_form.amount < 0:
                    error = True
                    for product in products:
                        if product.product.amount - product.amount * order_combo_add_form.amount < 0:
                            break
                        else:
                            product.product.amount += product.amount * order_combo_add_form.amount
                            product.product.save()
                    break
                else:
                    product.product.amount -= product.amount * order_combo_add_form.amount
                    product.product.save()
            
            combo_in_order_flag = False
            order_combo_items = OrderComboItem.objects.filter(order=order_id)
            for order_combo_item in order_combo_items:
                if order_combo_item.combo.name == combo.name:
                    order_combo_item.amount += 1
                    order_combo_item.save()
                    combo_in_order_flag = True
                    break
            
            order = Order.objects.get(id=order_id)
            order.phone_number.total += order_combo_add_form.combo.price * order_combo_add_form.amount
            
            order.phone_number.save()
            
            order_combo_add_form.order_id = order_id
            
            if error == False and combo_in_order_flag==False:
                order_combo_add_form.save()
                
        _add_samsa_gift(order, products_in_combo)

    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order_id=order_id)
    order_combos = OrderComboItem.objects.filter(order_id=order_id)
    order_item_add_form = OrderItemAddForm()
    order_combo_add_form = OrderComboAddForm()
    
    return render(request, "orders/orders_detail.html", {
        "section": "orders",
        "order": order,
        "order_items": order_items,
        'order_combos': order_combos,
        'products_in_combo': products_in_combo,
        "order_item_add_form": order_item_add_form,
        "order_combo_add_form": order_combo_add_form,
        "error": error
    })

@login_required    
def orders_delete_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        items = OrderItem.objects.filter(order_id=order.id)
        for item in items:
            product = Product.objects.get(id=item.product_id)
            product.amount += item.amount
            product.save()
        
        order_combos = OrderComboItem.objects.filter(order_id=order_id)
        products_in_combo_with_amount = {}
        for order_combo in order_combos:
            temp = ProductsInCombo.objects.filter(combo=order_combo.combo.id)
            products_in_combo_with_amount[order_combo.combo.name] = {'amount': order_combo.amount}
            for product in temp:
                products_in_combo_with_amount[order_combo.combo.name][product.product.name] = product.amount
                product.product.amount += product.amount
                product.save()
                
        order.phone_number.total -= order.get_total_cost()
        order.phone_number.save()
        
        order.delete()
        return redirect('orders_list')
    return render(request, "orders/orders_delete.html", {
        'section': "orders",
        "order": order,
        'order_id': order_id
    })
    
@login_required
def orders_item_delete_view(request, item_id):
    order_item = OrderItem.objects.get(id=item_id)
    order_id = order_item.order_id
    product = Product.objects.get(name=order_item.product.name)
    order = Order.objects.get(id=order_id)

    if request.method == "POST":
        product.amount += order_item.amount
        product.save()
        
        order.phone_number.total -= order_item.product.sell_price * order_item.amount
        order.phone_number.save() 
        
        order_item.delete()
        return redirect("orders_detail", order_id)
    return render(request, "orders/orders_delete.html", {
        "section": "orders",
        "order": order_item,
        "order_id": order.id 
    })
    
@login_required
def orders_combo_delete_view(request, combo_id, order_id):
    order_combo = OrderComboItem.objects.get(combo_id=combo_id, order_id=order_id)
    order_id = order_combo.order_id
    combo = Combo.objects.get(name=order_combo.combo.name)
    products = ProductsInCombo.objects.filter(combo=combo)
    order = Order.objects.get(id=order_id)
    
    if request.method == "POST":
        for product in products:
            product.product.amount += product.amount * order_combo.amount
            product.product.save()
            
        order.phone_number.total -= order_combo.get_cost()
        order.phone_number.save() 
        
        order_combo.delete()
        return redirect("orders_detail", order_id)
    
    return render(request, "orders/orders_delete.html", {
        "section": "orders",
        "order": order_combo,
        "order_id": order.id 
    })
    
def orders_column_update_view(request, order_id, order_stage):
    if request.method == "GET":
        order = Order.objects.get(id=order_id)
        order.stage = order_stage[-1]
        order.save()
        return JsonResponse({"saved": "OK"})
    