from django.urls import path
from . import views

# URL patterns for product-related views including browsing products, vendor inventory management,
# adding, editing, updating stock, and deleting products
urlpatterns = [
    path('browse/', views.browse_products, name='browse_products'),
    path('inventory/', views.vendor_inventory, name='vendor_inventory'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('update-stock/<int:product_id>/', views.update_stock, name='update_stock'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
