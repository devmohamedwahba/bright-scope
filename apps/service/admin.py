from django.contrib import admin
from .models import Service, ServiceFeature, Package, Addon, AddonCategory, Booking

class PackageInline(admin.TabularInline):
    model = Package
    extra = 1

class AddonInline(admin.TabularInline):
    model = Addon
    extra = 1

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'is_active']
    list_filter = ['service_type', 'is_active']
    search_fields = ['name', 'description']
    inlines = [ServiceFeatureInline, PackageInline, AddonInline]

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'package_type', 'price', 'is_active']
    list_filter = ['service', 'package_type', 'is_active']
    search_fields = ['name', 'service__name']
    list_editable = ['price', 'is_active']

@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'category', 'price', 'is_active']
    list_filter = ['service', 'category', 'is_active']
    search_fields = ['name', 'service__name']

@admin.register(AddonCategory)
class AddonCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'package', 'total_price', 'status', 'booking_date']
    list_filter = ['status', 'service', 'booking_date']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['addons']