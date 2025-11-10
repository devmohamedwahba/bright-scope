from django.contrib import admin
from .models import ContactSubmission, ContactMethod, OfficeLocation


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'service_type', 'created_at', 'is_resolved')
    list_filter = ('service_type', 'is_resolved', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    list_editable = ('is_resolved',)
    readonly_fields = ('created_at',)


# apps/contact_us/admin.py
from django.contrib import admin
from .models import ContactMethod, OfficeLocation


@admin.register(ContactMethod)
class ContactMethodAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'method_type',
        'value',
        'is_active',
        'order',
        'created_at'
    ]
    list_editable = ['is_active', 'order']
    list_filter = ['method_type', 'is_active', 'created_at']
    search_fields = ['title', 'title_ar', 'value', 'description']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'method_type',
                'is_active',
                'order'
            )
        }),
        ('English Content', {
            'fields': (
                'title',
                'description',
                'action_text',
            )
        }),
        ('Arabic Content', {
            'fields': (
                'title_ar',
                'description_ar',
                'action_text_ar',
            )
        }),
        ('Contact Details', {
            'fields': (
                'value',
                'icon',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        })
    )


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = [
        'office_name',
        'office_address',
        'is_primary',
        'created_at'
    ]
    list_editable = ['is_primary']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['office_name', 'office_name_ar', 'office_address', 'title']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Status', {
            'fields': ('is_primary',)
        }),
        ('English Content', {
            'fields': (
                'title',
                'description',
                'office_name',
                'office_address',
                'working_hours_name',
                'working_hours_weekdays',
            )
        }),
        ('Arabic Content', {
            'fields': (
                'title_ar',
                'description_ar',
                'office_name_ar',
                'office_address_ar',
                'working_hours_name_ar',
                'working_hours_weekdays_ar',
            )
        }),
        ('Additional Information', {
            'fields': (
                'icon',
                'google_maps_link',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        })
    )