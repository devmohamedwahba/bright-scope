from django.contrib import admin
from .models import ContactInfo, NewsletterSubscriber


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'phone_number', 'emergency_available', 'created_at']
    fieldsets = (
        ('English Content', {
            'fields': (
                'company_name', 'tagline',
                'address', 'building', 'office',
                'mon_fri_hours', 'saturday_hours', 'sunday_hours',
                'copyright_text'
            )
        }),
        ('Arabic Content', {
            'fields': (
                'company_name_ar', 'tagline_ar',
                'address_ar', 'building_ar', 'office_ar',
                'mon_fri_hours_ar', 'saturday_hours_ar', 'sunday_hours_ar',
                'copyright_text_ar'
            )
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'whatsapp_number', 'emergency_available')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url', 'twitter_url', 'youtube_url')
        }),
    )


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email']
    search_fields = ['email']
