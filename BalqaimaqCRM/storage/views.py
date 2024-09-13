from django.shortcuts import render, get_object_or_404, resolve_url, redirect, Http404

from .models import Product
from .forms import ProductForm, SupplyForm

def products_list_view(request):
    products_list = Product.objects.filter(available=True)
    return render(request, "storage/products_list.html", {
        "section": "storage",
        "products_list": products_list
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
    
def products_create_view(request):
    if request.method == "POST":
        # FIXME решить проблему с загрузкой картинок
        form = ProductForm(request.POST, files=request.FILES)
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
        product.save()
        return redirect('products_list')
    return render(request, "storage/products_delete.html", {
        'section': "storage",
        "product": product 
    })
    