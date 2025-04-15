from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('track/<int:order_id>/', views.track_order, name='track_order'),
    path('vendor-orders/', views.vendor_orders, name='vendor_orders'),
    path('mark-fulfilled/<int:detail_id>/', views.mark_fulfilled, name='mark_fulfilled'),
    path('assigned-orders/', views.assigned_orders, name='assigned_orders'),
    path('assigned-orders/<int:order_id>/', views.order_detail_delivery, name='order_detail_delivery'),


]
