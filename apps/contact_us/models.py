from django.db import models
from common.utils import BaseModel
from django.utils.translation import gettext_lazy as _


class ContactSubmission(BaseModel):
    SERVICE_TYPES = [
        ('consulting', 'Consulting'),
        ('support', 'Support'),
        ('others', 'Other'),

    ]

    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=17)
    email = models.EmailField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.service_type}"


class ContactMethod(BaseModel):
    METHOD_TYPES = [
        ('phone', 'Call Us'),
        ('whatsapp', 'WhatsApp Us'),
        ('email', 'Email Support'),
    ]

    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="fa-solid fa-phone"
    )
    method_type = models.CharField(max_length=20, choices=METHOD_TYPES, unique=True)

    # English fields
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    value = models.CharField(max_length=200, help_text="Phone number, email, or address")
    action_text = models.CharField(max_length=50, blank=True, help_text="e.g., 'Chat Now'")

    # Arabic fields
    title_ar = models.CharField(max_length=100, blank=True)
    description_ar = models.TextField(blank=True)
    action_text_ar = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'method_type']
        verbose_name = _('Contact Method')
        verbose_name_plural = _('Contact Methods')

    def __str__(self):
        return f"{self.title}"


class OfficeLocation(BaseModel):
    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="fa-solid fa-map-pin"
    )

    # English fields
    title = models.CharField(max_length=255, default="Visit Our Office")
    description = models.CharField(
        max_length=255,
        default="Come visit us at our Dubai headquarters for in-person consultations."
    )
    office_name = models.CharField(max_length=100, default="Business Bay, Dubai")
    office_address = models.CharField(max_length=100, default="United Arab Emirates")
    working_hours_name = models.CharField(max_length=100, default="Working Hours")
    working_hours_weekdays = models.CharField(max_length=200, default="Mon-Fri: 8AM-8PM | Sat: 9AM-6PM")

    # Arabic fields
    title_ar = models.CharField(max_length=255, blank=True, default="زيارة مكتبنا")
    description_ar = models.CharField(
        max_length=255,
        blank=True,
        default="تعال لزيارتنا في مقرنا الرئيسي في دبي للحصول على استشارات شخصية."
    )
    office_name_ar = models.CharField(max_length=100, blank=True, default="الخليج التجاري, دبي")
    office_address_ar = models.CharField(max_length=100, blank=True, default="الإمارات العربية المتحدة")
    working_hours_name_ar = models.CharField(max_length=100, blank=True, default="ساعات العمل")
    working_hours_weekdays_ar = models.CharField(max_length=200, blank=True,
                                                 default="الإثنين-الجمعة: 8 صباحاً-8 مساءً | السبت: 9 صباحاً-6 مساءً")

    google_maps_link = models.URLField(blank=True, null=True)
    is_primary = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Office Location')
        verbose_name_plural = _('Office Locations')

    def __str__(self):
        return self.office_name
