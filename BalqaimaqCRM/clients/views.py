from django.shortcuts import render, get_object_or_404, resolve_url, redirect

from .forms import ClientCreateForm, ClientUpdateForm
from .models import Client

def clients_list_order_view(request, slug):
    clients = Client.objects.all()
    clients = clients.order_by(slug)
    return render(request, 'clients/clients_list.html', {
        "section": "clients",
		"clients": clients
	})

def clients_list_view(request):
    clients = Client.objects.all()
    return render(request, 'clients/clients_list.html', {
        "section": "clients",
		"clients": clients
	})
    
def clients_detail_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/clients_detail.html', {
        "section": "clients",
		"client": client
    })
    
def clients_create_view(request):
    if request.method == "POST":
        form = ClientCreateForm(request.POST)
        if form.is_valid():
            form.save()
            url = resolve_url("clients_list")
            return redirect(url)
    else:
        form = ClientCreateForm()
    
    return render(request, "clients/clients_create.html", {
        "section": "clients",
        "form": form,
    })
    
def clients_update_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
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
            