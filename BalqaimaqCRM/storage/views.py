from django.shortcuts import render, get_object_or_404, resolve_url, redirect, Http404

from .models import Product, Combo, ProductsInCombo, Supply
from .forms import ProductForm, SupplyForm, ComboForm

def products_list_view(request):
    products_list = Product.objects.filter(available=True)
    combo_list = Combo.objects.filter(available=True)
    return render(request, "storage/products_list.html", {
        "section": "storage",
        "products_list": products_list,
        "combo_list": combo_list
    })
    
def products_table_view(request, slug=None):
    products_list = Product.objects.filter(available=True)
    if slug:
        products_list = products_list.order_by(slug)
    return render(request, "storage/products_table.html", {
        "section": "storage",
        "products_list": products_list
    })
    
def products_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not product.available:
        raise Http404("Страница не найдена")
    return render(request, "storage/products_detail.html", {
        "section": "storage",
        "product": product
    })
    
def combo_detail_view(request, pk):
    combo = Combo.objects.get(id=pk)
    products_in_combo = ProductsInCombo.objects.filter(combo=combo)
    return render(request, "storage/combo_detail.html", {
        "section": "storage",
        "combo": combo,
        "products_in_combo": products_in_combo
    })

def products_create_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            url = resolve_url("products_list")
            return redirect(url)
    else:
        form = ProductForm()
    return render(request, "storage/products_create.html", {
        "section": "storage",
        "form": form
    })
    
def combo_create_view(request):
    if request.method == "POST":
        form = ComboForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            url = resolve_url("products_list")
            return redirect(url)
    else:
        form = ComboForm()
    return render(request, "storage/combo_create.html", {
        "section": "storage",
        "form": form
    })

def products_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not product.available:
        raise Http404("Страница не найдена")
    if request.method == "POST":    
        form = ProductForm(instance=product,
                          data=request.POST)
        if form.is_valid():
            form.save()
            url = resolve_url("products_detail", pk)
            return redirect(url)
    else:
        form = ProductForm(instance=product)
        
    return render(request, "storage/products_update.html", {
        "section": "storage",
        "form": form,
        "product": product
    })
    
def combo_update_view(request, pk):
    combo = get_object_or_404(Combo, id=pk)
    if not combo.available:
        raise Http404("Страница не найдена")
    if request.method == "POST":    
        form = ComboForm(instance=combo,
                          data=request.POST)
        if form.is_valid():
            form.save()
            url = resolve_url("combo_detail", pk)
            return redirect(url)
    else:
        form = ComboForm(instance=combo)
        
    return render(request, "storage/combo_update.html", {
        "section": "storage",
        "form": form,
        "combo": combo
    })
    
def products_supply_view(request):
    if request.method == "POST":
        form = SupplyForm(data=request.POST)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            product = Product.objects.get(name=cd["product"])
            product.amount += cd["amount"]
            product.save()
            url = resolve_url("products_list")
            return redirect(url)
    else:
        form = SupplyForm()
    return render(request, "storage/products_supply.html", {
        "section": "storage",
        "form": form,
    })

def products_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not product.available:
        raise Http404("Страница не найдена")
    
    if request.method == "POST":
        product.available = False
        product.delete()
        return redirect('products_list')
    return render(request, "storage/products_delete.html", {
        'section': "storage",
        "product": product 
    })
    
def combo_delete_view(request, pk):
    combo = get_object_or_404(Combo, id=pk)
    if not combo.available:
        raise Http404("Страница не найдена")
    
    if request.method == "POST":
        combo.available = False
        combo.delete()
        return redirect('products_list')
    return render(request, "storage/products_delete.html", {
        'section': "storage",
        "product": combo
    })

def history_of_supply_view(request):
    supplies = Supply.objects.all()
    return render(request, "storage/history_of_supply.html", {
        "section": "storage",
        "supplies": supplies
    })