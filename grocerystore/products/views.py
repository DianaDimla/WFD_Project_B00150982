from django.shortcuts import render
from .models import Product

def browse_products(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    products = Product.objects.filter(is_available=True)

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category__icontains=category)

    return render(request, 'products/browse_products.html', {'products': products})