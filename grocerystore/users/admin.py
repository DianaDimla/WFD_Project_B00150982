from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Vendor, Customer
from .models import DeliveryAgent

# Inline admin descriptor for Vendor model linked to User
class VendorInline(admin.StackedInline):
    model = Vendor
    can_delete = False
    verbose_name_plural = 'Vendor'
    fk_name = 'user'
    extra = 1 

# Custom UserAdmin to include Vendor inline and display store name
class CustomUserAdmin(UserAdmin):
    inlines = (VendorInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_vendor')
    list_select_related = ('vendor',)

    def get_vendor(self, instance):
        return instance.vendor.store_name if hasattr(instance, 'vendor') else None
    get_vendor.short_description = 'Store Name'

# Admin registration for Vendor model with search and display options
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'phone')
    search_fields = ('store_name', 'user__username')
    raw_id_fields = ('user',) 

# Admin registration for Customer model with display options
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone')

# Unregister default User admin and register custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(DeliveryAgent)
