from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderDetail
from products.models import Product
from users.models import Customer, Vendor, DeliveryAgent
from users.decorators import delivery_agent_required
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# ----- Helper to get customer -----
def get_customer(user):
    try:
        return Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return None

# ----- View Cart -----
@login_required
def cart_view(request):
    customer = get_customer(request.user)
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total': round(total, 2)
    })

# ----- Add to Cart -----
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

# ----- Remove from Cart -----
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

# ----- Checkout -----
@login_required
def checkout_view(request):
    customer = get_customer(request.user)
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        payment_method = request.POST.get('payment_method')

        if not delivery_address or not payment_method:
            return render(request, 'orders/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'error': "Please provide delivery address and payment method."
            })

        # Save the order
        order = Order.objects.create(
            customer=customer,
            status='Processing',
            created_at=timezone.now(),
            delivery_address=delivery_address,
            payment_method=payment_method
        )

        # Save each cart item as an OrderDetail
        for item in cart_items:
            OrderDetail.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price_at_purchase=item['subtotal'] / item['quantity'] if item['quantity'] else 0
            )

        # Clear the cart
        request.session['cart'] = {}

        return redirect('order_success')

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': round(total, 2)
    })

# ----- Order Success Page -----
@login_required
def order_success_view(request):
    return render(request, 'orders/success.html')

# ----- Order History -----
@login_required
def order_history_view(request):
    customer = get_customer(request.user)
    if not customer:
        return redirect('login')

    orders = Order.objects.filter(customer=customer).order_by('-created_at')

    # Calculate total price for each order
    orders_with_totals = []
    for order in orders:
        order_details = OrderDetail.objects.filter(order=order)
        total = sum(od.price_at_purchase * od.quantity for od in order_details)
        order.total = total
        orders_with_totals.append(order)

    return render(request, 'orders/order_history.html', {'orders': orders_with_totals})

# ----- Track Order -----
@login_required
def track_order_view(request, order_id):
    customer = get_customer(request.user)
    if not customer:
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, customer=customer)

    order_details = OrderDetail.objects.filter(order=order)
    items = []
    total = 0
    for od in order_details:
        subtotal = od.price_at_purchase * od.quantity
        total += subtotal
        items.append({
            'product': od.product,
            'quantity': od.quantity,
            'subtotal': subtotal
        })

    order.items = items
    order.total = total

    return render(request, 'orders/track_order.html', {'order': order})

# ----- Vendor Orders -----
@login_required
def vendor_orders_view(request):
    try:
        vendor = request.user.vendor
    except Vendor.DoesNotExist:
        return redirect('login')

    # Get all order details with products from this vendor
    order_details = OrderDetail.objects.filter(product__vendor=vendor).select_related('order', 'product', 'order__customer')

    # Calculate total for each order detail's order
    orders_totals = {}
    for od in order_details:
        order_id = od.order.id
        orders_totals[order_id] = orders_totals.get(order_id, 0) + od.price_at_purchase * od.quantity

    # Pass order details and totals to template
    return render(request, 'orders/vendor_orders.html', {
        'order_details': order_details,
        'orders_totals': orders_totals,
    })

# ----- Fulfill Order -----
@login_required
def fulfill_order_view(request, order_detail_id):
    try:
        vendor = request.user.vendor
    except Vendor.DoesNotExist:
        return redirect('login')

    item = get_object_or_404(OrderDetail, id=order_detail_id, product__vendor=vendor)
    item.fulfilled = True
    item.save()

    # Remove delivery agent assignment logic to allow all delivery agents to see fulfilled orders
    # No assignment of delivery_agent to order here

    return redirect('vendor_orders')

# ----- Assigned Orders for Delivery Agent -----
@login_required
@delivery_agent_required
def assigned_orders_view(request):
    # Show all orders that have at least one fulfilled order detail and are ready for pickup
    # Adjusted to include orders with status 'Pending' or 'Processing' to match actual statuses
    orders = Order.objects.filter(
        details__fulfilled=True,
        status__in=['Pending', 'Processing']
    ).distinct().order_by('-created_at')
    return render(request, 'orders/assigned_orders.html', {'orders': orders})

@login_required
@delivery_agent_required
def claim_order_view(request, order_id):
    agent = request.user.deliveryagent
    order = get_object_or_404(Order, id=order_id, status='Processing', delivery_agent__isnull=True)
    order.delivery_agent = agent
    order.save()
    return redirect('assigned_orders')

# ----- Update Delivery Status -----
@login_required
@delivery_agent_required
def update_delivery_status(request, order_id):
    # Removed delivery_agent filter to allow all delivery agents to update any fulfilled order
    order = get_object_or_404(Order, id=order_id)

    # Calculate items and total for the order
    order_details = OrderDetail.objects.filter(order=order)
    items = []
    total = 0
    for od in order_details:
        subtotal = od.price_at_purchase * od.quantity
        total += subtotal
        items.append({
            'product': od.product,
            'quantity': od.quantity,
            'subtotal': subtotal
        })
    order.items = items
    order.total = total

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['In Transit', 'Delivered']:
            order.status = new_status
            order.save()
            return redirect('assigned_orders')

    return render(request, 'orders/order_detail_delivery.html', {'order': order})

# ----- Order Detail Delivery View -----
@login_required
@delivery_agent_required
def order_detail_delivery_view(request, order_id):
    # Removed delivery_agent filter to allow all delivery agents to view any fulfilled order
    order = get_object_or_404(Order, id=order_id)

    # Calculate items and total for the order
    order_details = OrderDetail.objects.filter(order=order)
    items = []
    total = 0
    for od in order_details:
        subtotal = od.price_at_purchase * od.quantity
        total += subtotal
        items.append({
            'product': od.product,
            'quantity': od.quantity,
            'subtotal': subtotal
        })
    order.items = items
    order.total = total

    return render(request, 'orders/order_detail_delivery.html', {'order': order})
