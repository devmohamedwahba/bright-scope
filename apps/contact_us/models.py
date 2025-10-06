from django.db import models
from common.utils import BaseModel


class ContactSubmission(BaseModel):
    SERVICE_TYPES = [
        ('residential', 'Residential Cleaning'),
        ('commercial', 'Commercial Cleaning'),
        ('deep_clean', 'Deep Cleaning'),
        ('move_in_out', 'Move In/Out Cleaning'),
        ('other', 'Other'),
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
        default="fa-solid fa-map-pin"
    )
    method_type = models.CharField(max_length=20, choices=METHOD_TYPES, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    value = models.CharField(max_length=200, help_text="Phone number, email, or address")
    action_text = models.CharField(max_length=50, blank=True, help_text="e.g., 'Chat Now'")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'method_type']

    def __str__(self):
        return f"{self.title}"


class OfficeLocation(BaseModel):
    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="fa-solid fa-map-pin"
    )
    title = models.CharField(max_length=255, default="Visit Our Office")
    description = models.CharField(max_length=255,
                                   default="Come visit us at our Dubai headquarters for in-person consultations.")
    office_name = models.CharField(max_length=100, default="Business Bay, Dubai")
    office_address = models.CharField(max_length=100, default="United Arab Emirates")

    working_hours_name = models.CharField(max_length=100, default="Working Hours")
    working_hours_weekdays = models.CharField(max_length=200, default="Mon-Fri: 8AM-8PM | Sat: 9AM-6PM")
    google_maps_link = models.URLField(blank=True, null=True)
    is_primary = models.BooleanField(default=True)

    def __str__(self):
        return self.office_name
