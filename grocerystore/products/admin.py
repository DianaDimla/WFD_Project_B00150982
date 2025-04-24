from django.contrib import admin
from .models import Product
from users.models import Vendor

# Admin configuration for Product model to customize list display, filters, and search
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'vendor', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    raw_id_fields = ('vendor',) 
    
    # Customize the form to limit vendor queryset if needed
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['vendor'].queryset = Vendor.objects.all()
        return form
