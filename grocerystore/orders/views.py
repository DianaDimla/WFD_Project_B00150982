from django.shortcuts import redirect
from products.models import Product
from django.shortcuts import render

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1  # increment qty

    request.session['cart'] = cart
    return redirect('browse_products')

def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    
    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'total': product.price * cart[str(product.id)]
        })

    return render(request, 'orders/cart.html', {'cart_items': cart_items})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect('cart')  # cart view name

