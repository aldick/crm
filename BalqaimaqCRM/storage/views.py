from django.shortcuts import render, get_object_or_404, resolve_url, redirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Product, Combo, ProductsInCombo, Supply
from .forms import ProductForm, SupplyForm, ComboForm, AddProductToComboForm

@login_required
def products_list_view(request):
    products_list = Product.objects.filter(available=True)
    combo_list = Combo.objects.filter(available=True)
    return render(request, "storage/products_list.html", {
        "section": "storage",
        "products_list": products_list,
        "combo_list": combo_list
    })
    
@login_required
def products_table_view(request, slug=None):
    products_list = Product.objects.filter(available=True)
    if slug:
        products_list = products_list.order_by(slug)
    return render(request, "storage/products_table.html", {
        "section": "storage",
        "products_list": products_list
    })
    
@login_required
def products_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not product.available:
        raise Http404("Страница не найдена")
    return render(request, "storage/products_detail.html", {
        "section": "storage",
        "product": product
    })
    
@login_required
def combo_detail_view(request, pk):
    combo = Combo.objects.get(id=pk)
    products_in_combo = ProductsInCombo.objects.filter(combo=combo)
    return render(request, "storage/combo_detail.html", {
        "section": "storage",
        "combo": combo,
        "products_in_combo": products_in_combo
    })

@login_required
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
    
@login_required
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

@login_required
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
    
@login_required
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
    
@login_required
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

@login_required
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
    
@login_required
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
    
@login_required
def add_product_to_combo_view(request, combo_id):
    combo = get_object_or_404(Combo, id=combo_id)
    if not combo.available:
        raise Http404("Страница не найдена")
    
    products_in_combo = ProductsInCombo.objects.filter(combo=combo)
    
    if request.method == "POST":
        form = AddProductToComboForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            cd = form.cleaned_data
            product_id = cd['product']
            amount = cd['amount']
            new_product = ProductsInCombo.objects.create(
                product=product_id,
                combo=combo,
                amount=amount
            )
            
            url = resolve_url("combo_detail", combo_id)
            return redirect(url)
    else:
        form = AddProductToComboForm()
        
    return render(request, "storage/combo_add_product.html", {
        "section": "storage",
        "combo": combo,
        "products_in_combo": products_in_combo,
        "form": form,
    })
    
@login_required
def remove_product_from_combo_view(request, combo_id, product_id):
    combo = get_object_or_404(Combo, id=combo_id)
    if not combo.available:
        raise Http404("Страница не найдена")
    
    product=Product.objects.get(id=product_id)

    if request.method == "POST":
        products_in_combo = ProductsInCombo.objects.filter(combo=combo, product=product)
        
        for product in products_in_combo:
            product.delete()
        
        url = resolve_url("combo_detail", combo_id)
        return redirect(url)        
            
    return render(request, "storage/combo_remove_product.html", {
        'section': "storage",
        "product": product
    })


@login_required
def history_of_supply_view(request):
    supplies = Supply.objects.all()
    return render(request, "storage/history_of_supply.html", {
        "section": "storage",
        "supplies": supplies
    })