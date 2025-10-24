from django.db import models
from common.utils import BaseModel



class ContactInfo(BaseModel):
    company_name = models.CharField(max_length=200, default="Bright Scope UAE")
    tagline = models.TextField(
        default="Your trusted cleaning and pest control partner in Dubai. 15+ years of excellence from Egypt to the UAE, serving thousands of satisfied customers.")
    phone_number = models.CharField(max_length=20, default="+971 XXX XXX XXX")
    whatsapp_number = models.CharField(max_length=20, default="+971 XXX XXX XXX")
    address = models.TextField(default="Business Bay, Dubai, UAE")
    building = models.CharField(max_length=100, default="Building XYZ")
    office = models.CharField(max_length=50, default="Office 123")

    # Working Hours
    mon_fri_hours = models.CharField(max_length=100, default="8:00 AM - 8:00 PM")
    saturday_hours = models.CharField(max_length=100, default="9:00 AM - 6:00 PM")
    sunday_hours = models.CharField(max_length=100, default="10:00 AM - 5:00 PM")

    # Emergency Service
    emergency_available = models.BooleanField(default=True)

    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    copyright_text = models.CharField(max_length=200, default="© 2024 Bright Scope Dubai. All rights reserved.")

    class Meta:
        verbose_name_plural = "Contact Info"
        ordering = ['-created_at']



class NewsletterSubscriber(BaseModel):
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email
