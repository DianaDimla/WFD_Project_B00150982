from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import forms

from .models import Product
from .forms import ProductForm
from users.models import Vendor

def browse_products(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    products = Product.objects.filter(is_available=True)

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category__icontains=category)

    return render(request, 'products/browse_products.html', {'products': products})

@login_required
def vendor_inventory(request):
    try:
        vendor = request.user.vendor
    except:
        return redirect('login')

    products = Product.objects.filter(vendor=vendor)
    return render(request, 'products/vendor_inventory.html', {'products': products})

@login_required
def add_product(request):
    try:
        vendor = request.user.vendor
    except:
        return redirect('login')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.is_available = True
            product.save()
            return redirect('browse_products')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    try:
        vendor = request.user.vendor
    except:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id, vendor=vendor)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.is_available = True
            # Assign uploaded image file explicitly to ensure it is saved
            if 'image' in form.cleaned_data:
                product.image = form.cleaned_data['image']
            product.save()
            return redirect('vendor_inventory')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

@login_required
def update_stock(request, product_id):
    try:
        vendor = request.user.vendor
    except:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id, vendor=vendor)

    if request.method == 'POST':
        new_stock = request.POST.get('stock')
        if new_stock.isdigit():
            product.stock = int(new_stock)
            product.save()
    return redirect('vendor_inventory')

@login_required
def delete_product(request, product_id):
    try:
        vendor = request.user.vendor
    except:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id, vendor=vendor)

    if request.method == 'POST':
        product.delete()
        return redirect('vendor_inventory')

    return render(request, 'products/delete_product.html', {'product': product})

