from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Service, ServiceFeature, Package, Addon, AddonCategory, Booking, ServiceContent, ServiceRating


class PackageInline(admin.TabularInline):
    model = Package
    extra = 1
    fields = ['name', 'name_ar', 'package_type', 'price', 'is_active', 'order']
    verbose_name = _("Package")
    verbose_name_plural = _("Packages")


class AddonInline(admin.TabularInline):
    model = Addon
    extra = 1
    fields = ['name', 'name_ar', 'category', 'price', 'is_active', 'order']
    verbose_name = _("Addon")
    verbose_name_plural = _("Addons")


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ['name', 'name_ar', 'description', 'description_ar', 'icon', 'order']
    verbose_name = _("Feature")
    verbose_name_plural = _("Features")


class ServiceContentInline(admin.TabularInline):
    model = ServiceContent
    extra = 1
    fields = ['name', 'name_ar', 'order']
    verbose_name = _("Content")
    verbose_name_plural = _("Contents")


class ServiceRatingInline(admin.TabularInline):
    model = ServiceRating
    extra = 1
    fields = ['name', 'name_ar', 'description', 'description_ar', 'icon', 'order']
    verbose_name = _("Rating")
    verbose_name_plural = _("Ratings")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'service_type', 'is_active', 'created_at']
    list_filter = ['service_type', 'is_active', 'created_at']
    search_fields = ['name', 'name_ar', 'description', 'description_ar']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ServiceFeatureInline, ServiceContentInline, ServiceRatingInline, PackageInline, AddonInline]

    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'name',
                'name_ar',
                'service_type',
                'start_price',
                'icon',
                'is_active'
            )
        }),
        (_('English Content'), {
            'fields': (
                'description',
                'hero_title',
                'sub_hero_title',
                'hero_description',
            )
        }),
        (_('Arabic Content'), {
            'fields': (
                'description_ar',
                'hero_title_ar',
                'sub_hero_title_ar',
                'hero_description_ar',
            )
        }),
        (_('Media'), {
            'fields': ('image',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'service', 'order', 'created_at']
    list_filter = ['service', 'created_at']
    search_fields = ['name', 'name_ar', 'description', 'description_ar', 'service__name']
    list_editable = ['order']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('service', 'order')
        }),
        (_('English Content'), {
            'fields': ('name', 'description')
        }),
        (_('Arabic Content'), {
            'fields': ('name_ar', 'description_ar')
        }),
        (_('Additional'), {
            'fields': ('icon',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ServiceContent)
class ServiceContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'service', 'order', 'created_at']
    list_filter = ['service', 'created_at']
    search_fields = ['name', 'name_ar', 'service__name']
    list_editable = ['order']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('service', 'order')
        }),
        (_('English Content'), {
            'fields': ('name',)
        }),
        (_('Arabic Content'), {
            'fields': ('name_ar',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ServiceRating)
class ServiceRatingAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'service', 'order', 'created_at']
    list_filter = ['service', 'created_at']
    search_fields = ['name', 'name_ar', 'description', 'description_ar', 'service__name']
    list_editable = ['order']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('service', 'order')
        }),
        (_('English Content'), {
            'fields': ('name', 'description')
        }),
        (_('Arabic Content'), {
            'fields': ('name_ar', 'description_ar')
        }),
        (_('Additional'), {
            'fields': ('icon',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'service', 'package_type', 'price', 'is_active', 'order']
    list_filter = ['service', 'package_type', 'is_active', 'created_at']
    search_fields = ['name', 'name_ar', 'description', 'description_ar', 'service__name']
    list_editable = ['price', 'is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'service',
                'package_type',
                'price',
                'is_active',
                'order'
            )
        }),
        (_('English Content'), {
            'fields': (
                'name',
                'description',
                'square_feet',
                'duration'
            )
        }),
        (_('Arabic Content'), {
            'fields': (
                'name_ar',
                'description_ar',
                'square_feet_ar',
                'duration_ar'
            )
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(AddonCategory)
class AddonCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_ar', 'description', 'description_ar']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('is_active', 'order')
        }),
        (_('English Content'), {
            'fields': ('name', 'description')
        }),
        (_('Arabic Content'), {
            'fields': ('name_ar', 'description_ar')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'service', 'category', 'price', 'is_active', 'order']
    list_filter = ['service', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'name_ar', 'description', 'description_ar', 'service__name']
    list_editable = ['price', 'is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'service',
                'category',
                'price',
                'is_active',
                'order'
            )
        }),
        (_('English Content'), {
            'fields': ('name', 'description')
        }),
        (_('Arabic Content'), {
            'fields': ('name_ar', 'description_ar')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'package', 'total_price', 'status', 'booking_date', 'created_at']
    list_filter = ['status', 'service', 'booking_date', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone', 'service__name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    filter_horizontal = ['addons']

    fieldsets = (
        (_('Customer Information'), {
            'fields': (
                'customer_name',
                'customer_email',
                'customer_phone',
                'address'
            )
        }),
        (_('Booking Details'), {
            'fields': (
                'service',
                'package',
                'addons',
                'booking_date',
                'special_requests'
            )
        }),
        (_('Pricing'), {
            'fields': ('total_price',)
        }),
        (_('Status'), {
            'fields': ('status',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
