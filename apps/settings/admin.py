from django.contrib import admin
from .models import ContactInfo, NewsletterSubscriber


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'phone_number']

    def has_add_permission(self, request):
        # Allow only one contact info instance
        if ContactInfo.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email']
    search_fields = ['email']