from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Vendor, Customer

class VendorInline(admin.StackedInline):
    model = Vendor
    can_delete = False
    verbose_name_plural = 'Vendor'
    fk_name = 'user'
    extra = 1  # Shows 1 empty form by default

class CustomUserAdmin(UserAdmin):
    inlines = (VendorInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_vendor')
    list_select_related = ('vendor',)

    def get_vendor(self, instance):
        return instance.vendor.store_name if hasattr(instance, 'vendor') else None
    get_vendor.short_description = 'Store Name'

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'phone')
    search_fields = ('store_name', 'user__username')
    raw_id_fields = ('user',)  # Helps with user selection

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone')

# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)