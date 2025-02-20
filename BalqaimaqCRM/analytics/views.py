import datetime
from calendar import monthrange
from django.shortcuts import render, HttpResponse, get_object_or_404, resolve_url, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from orders.models import Order, OrderItem
from storage.models import Product, Supply
from clients.models import Worker
from clients.forms import WorkerCreateForm, WorkerUpdateForm

@login_required
def selling_view(request):
    return render(request, "analytics/analytics_selling.html", {
		"section": "analytics"
	})

@login_required
def products_view(request):
    return render(request, "analytics/analytics_products.html", {
        "section": "analytics"
    })

#TODO доработать эту страницу
@login_required
def workers_list_view(request):
    date = request.GET.get("date", "cw")
    days, start, end = _get_days(date)
    
    workers = Worker.objects.filter(is_active=True)
    supplies = {}
    for worker in workers:
        supplies[worker.phone_number] = {}
        for supply in worker.supplies.filter(created_at__gt=start).filter(created_at__lt=end):
            try:
                supplies[worker.phone_number][supply.product] += supply.amount
            except KeyError:
                supplies[worker.phone_number][supply.product] = supply.amount
    return render(request, "analytics/analytics_workers_list.html", {
        "workers": workers,
        "supplies": supplies,
        "section": "analytics"
    })
  
@login_required  
def workers_detail_view(request, phone_number):
    worker = get_object_or_404(Worker, pk=phone_number)
    if not worker.is_active:
        raise Http404("Страница не найдена")
    
    date = request.GET.get("date", "cw")
    days, start, end = _get_days(date)
    
    supplies = {}
    supplies[worker.phone_number] = {}
    for supply in worker.supplies.filter(created_at__gt=start).filter(created_at__lt=end):
        try:
            supplies[worker.phone_number][supply.product.name] += supply.amount
        except KeyError:
            supplies[worker.phone_number][supply.product.name] = supply.amount
            
    return render(request, 'analytics/analytics_workers_detail.html', {
        "section": "analytics",
        'worker': worker,
        'supplies': supplies,
    })

@login_required
def workers_create_view(request):
    if request.method == "POST":
        form = WorkerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            url = resolve_url('analytics_workers_list')
            return redirect(url)
    else:    
        form = WorkerCreateForm() 
        
    return render(request, "analytics/analytics_workers_create.html", {
        "section": "analytics",
        "form": form
    })

@login_required
def workers_update_view(request, phone_number):
    worker = get_object_or_404(Worker, pk=phone_number)
    if not worker.is_active:
        raise Http404("Страница не найдена")
    if request.method == "POST":
        form = WorkerUpdateForm(instance=worker,
                                data=request.POST)
        if form.is_valid():
            form.save()

            url = resolve_url("analytics_workers_detail", phone_number)
            return redirect(url)
    else:
        form = WorkerUpdateForm(instance=worker)

    return render(request, "analytics/analytics_workers_update.html", {
        "section": "analytics",
        "form": form,
        "worker": worker
    })
    
@login_required
def workers_delete_view(request, phone_number):
    worker = get_object_or_404(Worker, pk=phone_number)
    if not worker.is_active:
        raise Http404("Страница не найдена")

    if request.method == "POST":
        worker.delete()
        return redirect('analytics_workers_list')
    return render(request, "analytics/analytics_workers_delete.html", {
        'section': "analytics",
        "worker": worker,
        "worker_id": phone_number
    })

def _get_days(date):
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
            month = (datetime.date.today().month + 1) % 12 - 1 
            days = monthrange(current_year, month)[1]
            start = datetime.date.today() - datetime.timedelta(datetime.date.today().day) - datetime.timedelta(days) + datetime.timedelta(1)
    end = start + datetime.timedelta(days)
    return days, start, end
    
def get_selling(request, date):
    orders_dict = {'days': {}}
    days, start, end = _get_days(date)
    orders = Order.objects.filter(created_at__gt=start).filter(created_at__lt=end)
    total_sum = 0
    
    
    for i in range(1, days+1):
        orders_dict["days"][i] = 0
        
    if date[1] == 'w':         
        for order in orders:
            total_sum += order.get_total_cost()
            orders_dict["days"][order.created_at.weekday()+1] += order.get_total_cost()
    elif date[1] == 'm':
        for order in orders:
            total_sum += order.get_total_cost()
            orders_dict["days"][order.created_at.day] = order.get_total_cost()
         
    orders_dict["total_sum"] = total_sum
    return JsonResponse(orders_dict)
    
def get_products(request, date):
    products_list = {}
    days, start, end = _get_days(date)
    orders = Order.objects.filter(created_at__gt=start).filter(created_at__lt=end)
    
    products = Product.objects.all()
    for product in products:
        products_list[product.name] = 0
    
    order_items = OrderItem.objects.all()
    for item in order_items:
        if item.order.created_at.date() >= start and item.order.created_at.date() < end:
            products_list[item.product.name] += item.amount
    
    return JsonResponse(products_list)

def get_types_of_orders(request, date):
    types_of_orders = {}
    days, start, end = _get_days(date)
    orders = Order.objects.filter(created_at__gt=start).filter(created_at__lt=end)
    for order in orders:
        try:
            types_of_orders[order.TYPE_OF_ORDERS[order.type_of_order]] += 1
        except KeyError:
            types_of_orders[order.TYPE_OF_ORDERS[order.type_of_order]] = 1
    return JsonResponse(types_of_orders)

def get_types_of_payments(request, date):
    types_of_payments = {}
    days, start, end = _get_days(date)
    orders = Order.objects.filter(created_at__gt=start).filter(created_at__lt=end)
    for order in orders:
        try:
            types_of_payments[order.TYPE_OF_PAYMENTS[order.type_of_payment]] += 1
        except KeyError:
            types_of_payments[order.TYPE_OF_PAYMENTS[order.type_of_payment]] = 1
    return JsonResponse(types_of_payments)
    
def get_workers_supplies(request, phone_number, date):
    days, start, end = _get_days(date)
    workers_supplies = {'days': days , 'supplies': {}}

    products = Product.objects.filter(available=True)
    for product in products:
        workers_supplies['supplies'][product.name] = [0] * (days) 
    
    supplies = Supply.objects.filter(worker=phone_number).filter(created_at__gt=start).filter(created_at__lt=end)
    
    if days == 7:
        for supply in supplies:
            workers_supplies['supplies'][supply.product.name][supply.created_at.weekday()] += int(supply.amount)
    else:
        for supply in supplies:
            workers_supplies['supplies'][supply.product.name][supply.created_at.day-1] += int(supply.amount)
            
    return JsonResponse(workers_supplies)
            