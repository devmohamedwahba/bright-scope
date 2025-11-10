from django.db import models
from common.utils import BaseModel
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _


class Service(BaseModel):
    SERVICE_TYPES = [
        ('home_cleaning', 'Home Cleaning'),
        ('deep_cleaning', 'Deep Cleaning'),
        ('pest_control', 'Pest Control'),
        ('post_construction', 'Post Construction Cleaning'),
        ('office_commercial', 'Office & Commercial'),
    ]

    # English fields
    name = models.CharField(max_length=100)
    description = models.TextField()
    hero_title = models.CharField(max_length=200, blank=True)
    sub_hero_title = models.CharField(max_length=200, blank=True, null=True)
    hero_description = models.TextField(blank=True)

    # Arabic fields
    name_ar = models.CharField(max_length=100, blank=True, verbose_name=_('Name (Arabic)'))
    description_ar = models.TextField(blank=True, verbose_name=_('Description (Arabic)'))
    hero_title_ar = models.CharField(max_length=200, blank=True, verbose_name=_('Hero Title (Arabic)'))
    sub_hero_title_ar = models.CharField(max_length=200, blank=True, null=True,
                                         verbose_name=_('Sub Hero Title (Arabic)'))
    hero_description_ar = models.TextField(blank=True, verbose_name=_('Hero Description (Arabic)'))

    start_price = models.IntegerField(null=True, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    icon = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_name(self):
        """Return name based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.name_ar:
            return self.name_ar
        return self.name

    def get_description(self):
        """Return description based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.description_ar:
            return self.description_ar
        return self.description

    def get_hero_title(self):
        """Return hero title based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.hero_title_ar:
            return self.hero_title_ar
        return self.hero_title

    def get_sub_hero_title(self):
        """Return sub hero title based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.sub_hero_title_ar:
            return self.sub_hero_title_ar
        return self.sub_hero_title

    def get_hero_description(self):
        """Return hero description based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.hero_description_ar:
            return self.hero_description_ar
        return self.hero_description


class ServiceFeature(BaseModel):
    service = models.ForeignKey(Service, related_name='features', on_delete=models.CASCADE)

    # English fields
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Arabic fields
    name_ar = models.CharField(max_length=200, blank=True, verbose_name=_('Name (Arabic)'))
    description_ar = models.TextField(blank=True, verbose_name=_('Description (Arabic)'))

    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"

    def get_name(self):
        """Return name based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.name_ar:
            return self.name_ar
        return self.name

    def get_description(self):
        """Return description based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.description_ar:
            return self.description_ar
        return self.description


class ServiceContent(BaseModel):
    service = models.ForeignKey(Service, related_name='contents', on_delete=models.CASCADE)

    # English fields
    name = models.CharField(max_length=200)

    # Arabic fields
    name_ar = models.CharField(max_length=200, blank=True, verbose_name=_('Name (Arabic)'))

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"

    def get_name(self):
        """Return name based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.name_ar:
            return self.name_ar
        return self.name


class ServiceRating(BaseModel):
    service = models.ForeignKey(Service, related_name='ratings', on_delete=models.CASCADE)

    # English fields
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    # Arabic fields
    name_ar = models.CharField(max_length=200, blank=True, verbose_name=_('Name (Arabic)'))
    description_ar = models.CharField(max_length=200, blank=True, verbose_name=_('Description (Arabic)'))

    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"

    def get_name(self):
        """Return name based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.name_ar:
            return self.name_ar
        return self.name

    def get_description(self):
        """Return description based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.description_ar:
            return self.description_ar
        return self.description


class Package(BaseModel):
    PACKAGE_TYPES = [
        ('studio', 'Studio'),
        ('2bhk', '2 BHK'),
        ('villa', 'Villa'),
        ('office', 'Office'),
        ('custom', 'Custom'),
    ]

    service = models.ForeignKey(Service, related_name='packages', on_delete=models.CASCADE)

    # English fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    square_feet = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    # Arabic fields
    name_ar = models.CharField(max_length=100, blank=True, verbose_name=_('Name (Arabic)'))
    description_ar = models.TextField(blank=True, verbose_name=_('Description (Arabic)'))
    square_feet_ar = models.CharField(max_length=100, blank=True, verbose_name=_('Square Feet (Arabic)'))
    duration_ar = models.CharField(max_length=100, blank=True, verbose_name=_('Duration (Arabic)'))

    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return f"{self.service.name} - {self.name}"

    def get_name(self):
        """Return name based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.name_ar:
            return self.name_ar
        return self.name

    def get_description(self):
        """Return description based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.description_ar:
            return self.description_ar
        return self.description

    def get_square_feet(self):
        """Return square feet based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.square_feet_ar:
            return self.square_feet_ar
        return self.square_feet

    def get_duration(self):
        """Return duration based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.duration_ar:
            return self.duration_ar
        return self.duration


class AddonCategory(BaseModel):
    # English fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Arabic fields
    name_ar = models.CharField(max_length=100, blank=True, verbose_name=_('Name (Arabic)'))
    description_ar = models.TextField(blank=True, verbose_name=_('Description (Arabic)'))

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Addon Categories"

    def __str__(self):
        return self.name

    def get_name(self):
        """Return name based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.name_ar:
            return self.name_ar
        return self.name

    def get_description(self):
        """Return description based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.description_ar:
            return self.description_ar
        return self.description


class Addon(BaseModel):
    service = models.ForeignKey(Service, related_name='addons', on_delete=models.CASCADE)
    category = models.ForeignKey(AddonCategory, related_name='addons', on_delete=models.CASCADE, null=True, blank=True)

    # English fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Arabic fields
    name_ar = models.CharField(max_length=100, blank=True, verbose_name=_('Name (Arabic)'))
    description_ar = models.TextField(blank=True, verbose_name=_('Description (Arabic)'))

    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"

    def get_name(self):
        """Return name based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.name_ar:
            return self.name_ar
        return self.name

    def get_description(self):
        """Return description based on current language"""
        from django.utils import translation
        if translation.get_language() == 'ar' and self.description_ar:
            return self.description_ar
        return self.description

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    addons = models.ManyToManyField(Addon, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    address = models.TextField()
    booking_date = models.DateTimeField()
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.service.name} - {self.package.name}"
