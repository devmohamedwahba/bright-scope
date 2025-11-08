from django.db import models
from common.utils import BaseModel
from django.utils.translation import gettext_lazy as _


class ContactInfo(BaseModel):
    # Company Information - English
    company_name = models.CharField(max_length=200, default="Bright Scope UAE")
    tagline = models.TextField(
        default="Your trusted cleaning and pest control partner in Dubai. 15+ years of excellence from Egypt to the UAE, serving thousands of satisfied customers.")

    # Company Information - Arabic
    company_name_ar = models.CharField(max_length=200, default="برايت سكوب الإمارات")
    tagline_ar = models.TextField(
        default="شريكك الموثوق في التنظيف ومكافحة الحشرات في دبي. أكثر من 15 عامًا من التميز من مصر إلى الإمارات، نخدم آلاف العملاء الراضين.")

    # Contact Details
    phone_number = models.CharField(max_length=20, default="+971 XXX XXX XXX")
    whatsapp_number = models.CharField(max_length=20, default="+971 XXX XXX XXX")

    # Address - English
    address = models.TextField(default="Business Bay, Dubai, UAE")
    building = models.CharField(max_length=100, default="Building XYZ")
    office = models.CharField(max_length=50, default="Office 123")

    # Address - Arabic
    address_ar = models.TextField(default="الخليج التجاري، دبي، الإمارات")
    building_ar = models.CharField(max_length=100, default="مبنى XYZ")
    office_ar = models.CharField(max_length=50, default="المكتب 123")

    # Working Hours - English
    mon_fri_hours = models.CharField(max_length=100, default="8:00 AM - 8:00 PM")
    saturday_hours = models.CharField(max_length=100, default="9:00 AM - 6:00 PM")
    sunday_hours = models.CharField(max_length=100, default="10:00 AM - 5:00 PM")

    # Working Hours - Arabic
    mon_fri_hours_ar = models.CharField(max_length=100, default="٨:٠٠ ص - ٨:٠٠ م")
    saturday_hours_ar = models.CharField(max_length=100, default="٩:٠٠ ص - ٦:٠٠ م")
    sunday_hours_ar = models.CharField(max_length=100, default="١٠:٠٠ ص - ٥:٠٠ م")

    # Emergency Service
    emergency_available = models.BooleanField(default=True)

    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    # Copyright - English & Arabic
    copyright_text = models.CharField(max_length=200, default="© 2024 Bright Scope Dubai. All rights reserved.")
    copyright_text_ar = models.CharField(max_length=200, default="© ٢٠٢٤ برايت سكوب دبي. جميع الحقوق محفوظة.")

    class Meta:
        verbose_name_plural = "Contact Info"
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name






class NewsletterSubscriber(BaseModel):
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email
