from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Order, OrderDetail
from products.models import Product
from users.models import Customer, Vendor, DeliveryAgent
from users.decorators import delivery_agent_required

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

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')  # or show a message

    # Get the current logged-in customer
    try:
        customer = request.user.customer
    except:
        return redirect('login')

    # Create order
    order = Order.objects.create(customer=customer)

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderDetail.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price_at_purchase=product.price
        )

        # Optional: reduce stock
        product.stock -= quantity
        product.save()

    # Clear cart
    request.session['cart'] = {}

    return render(request, 'orders/checkout_success.html', {'order': order})

@login_required
def order_history(request):
    try:
        customer = request.user.customer
    except:
        return redirect('login')  # Fallback just in cases 

    orders = Order.objects.filter(customer=customer).order_by('-created_at')

    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def track_order(request, order_id):
    try:
        customer = request.user.customer
    except:
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, customer=customer)

    return render(request, 'orders/track_order.html', {'order': order})

@login_required
def vendor_orders(request):
    try:
        vendor = request.user.vendor
    except:
        return redirect('login')

    # Get all order details for products sold by this vendor
    order_items = OrderDetail.objects.filter(product__vendor=vendor).select_related('order', 'product', 'order__customer')

    return render(request, 'orders/vendor_orders.html', {'order_items': order_items})

@login_required
def mark_fulfilled(request, detail_id):
    try:
        vendor = request.user.vendor
    except:
        return redirect('login')

    item = get_object_or_404(OrderDetail, id=detail_id, product__vendor=vendor)

    item.fulfilled = True
    item.save()

    return redirect('vendor_orders')

@login_required
@delivery_agent_required
def assigned_orders(request):
    agent = request.user.deliveryagent
    orders = Order.objects.filter(delivery_agent=agent).order_by('-created_at')
    return render(request, 'orders/assigned_orders.html', {'orders': orders})

@login_required
@delivery_agent_required
def order_detail_delivery(request, order_id):
    agent = request.user.deliveryagent
    order = get_object_or_404(Order, id=order_id, delivery_agent=agent)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['In Transit', 'Delivered']:
            order.status = new_status
            order.save()
            return redirect('assigned_orders')

    return render(request, 'orders/order_detail_delivery.html', {'order': order})


