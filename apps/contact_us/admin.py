from django.contrib import admin
from .models import ContactSubmission, ContactMethod, OfficeLocation


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'service_type', 'created_at', 'is_resolved')
    list_filter = ('service_type', 'is_resolved', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    list_editable = ('is_resolved',)
    readonly_fields = ('created_at',)


@admin.register(ContactMethod)
class ContactMethodAdmin(admin.ModelAdmin):
    list_display = ('method_type', 'title','description', 'value', 'is_active', 'order')
    list_filter = ('method_type', 'is_active')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'method_type')


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ('title','description','office_name', 'office_address', 'is_primary')
    list_editable = ('is_primary',)
