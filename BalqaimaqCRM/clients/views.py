from django.shortcuts import render, get_object_or_404, resolve_url, redirect, Http404
from django.db.models import Q

from .forms import ClientCreateForm, ClientUpdateForm, ClientSelectForm
from .models import Client

def clients_list_order_view(request, slug):
    clients = Client.objects.filter(is_active=True)
    clients = clients.order_by(-slug)
    return render(request, 'clients/clients_list.html', {
        "section": "clients",
		"clients": clients
	})

def clients_list_view(request):
    clients = Client.objects.filter(is_active=True)
    return render(request, 'clients/clients_list.html', {
        "section": "clients",
		"clients": clients
	})
    
def clients_detail_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not client.is_active:
        raise Http404("Страница не найдена")
    return render(request, 'clients/clients_detail.html', {
        "section": "clients",
		"client": client
    })
    
def clients_create_view(request, slug=None):
    
    if request.method == "POST":    
        form = ClientCreateForm(request.POST)
        if form.is_valid():
            form.save()
            url = resolve_url("clients_list")
            if slug == "order":
                return redirect(f'../../../orders/create/?phone_number=%2B{form.cleaned_data["phone_number"][1:]}')
                # url = "orders_create"
                # phone_number = form.cleaned_data["phone_number"][1:]
                # get = "phone_number=%2B"
                # return redirect(url, get + phone_number)
            return redirect(url)
    elif 'phone_number' in request.GET:
        phone_number = Client.objects.create(phone_number=request.GET.get("phone_number"))
        form = ClientCreateForm(instance=phone_number)
        phone_number.delete()
        
    else:
        form = ClientCreateForm()
    
    return render(request, "clients/clients_create.html", {
        "section": "clients",
        "form": form,
    })
    
def clients_update_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not client.is_active:
        raise Http404("Страница не найдена")
    if request.method == "POST":    
        form = ClientUpdateForm(instance=client,
                          data=request.POST)
        if form.is_valid():
            form.save()
            url = resolve_url("clients_detail", pk)
            return redirect(url)
    else:
        form = ClientUpdateForm(instance=client)
        
    return render(request, "clients/clients_update.html", {
        "section": "clients",
        "form": form,
        "client": client
    })
    
def clients_delete_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not client.is_active:
        raise Http404("Страница не найдена")
    
    if request.method == "POST":
        client.is_active = False
        client.save()
        return redirect('clients_list')
    return render(request, "clients/clients_delete.html", {
        'section': "clients",
        "client": client
    })
    
def clients_select_view(request, phone_number=None):
    form = ClientSelectForm()
    clients = Client.objects.filter(phone_number="1")
    if 'phone_number' in request.GET:
        q = request.GET['phone_number']
        multiple_q = Q(Q(phone_number__icontains=q) | Q(name__icontains=q))
        clients = Client.objects.filter(multiple_q).filter(is_active=True)
        
        phone_number = Client.objects.create(phone_number=request.GET.get("phone_number"))
        form = ClientSelectForm(instance=phone_number)
        phone_number.delete()
    
    return render(request, "clients/clients_select.html", {
        "section": "orders",
        "clients": clients,
        "form": form,
        "phone_number": request.GET.get('phone_number')
    })
    