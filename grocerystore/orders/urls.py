from django.urls import path
from . import views

urlpatterns = [
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/', views.order_success_view, name='order_success'),

    # Customer Order History & Tracking
    path('order-history/', views.order_history_view, name='order_history'),
    path('track-order/<int:order_id>/', views.track_order_view, name='track_order'),

    # Vendor Orders
    path('vendor/orders/', views.vendor_orders_view, name='vendor_orders'),
    path('vendor/orders/fulfill/<int:order_detail_id>/', views.fulfill_order_view, name='fulfill_order'),

    # Delivery Agent
    path('delivery/assigned/', views.assigned_orders_view, name='assigned_orders'),
    path('delivery/claim/<int:order_id>/', views.claim_order_view, name='claim_order'),
    path('delivery/update-status/<int:order_id>/', views.update_delivery_status, name='update_delivery_status'),
    path('delivery/order/<int:order_id>/', views.order_detail_delivery_view, name='order_detail_delivery'),
]
