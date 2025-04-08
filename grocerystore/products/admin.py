from django.contrib import admin
from .models import Product
from users.models import Vendor

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'vendor', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    raw_id_fields = ('vendor',)  # This fixes the template rendering error
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['vendor'].queryset = Vendor.objects.all()
        return form