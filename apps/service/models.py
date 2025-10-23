from django.db import models
from common.utils import BaseModel


class Service(BaseModel):
    SERVICE_TYPES = [
        ('home_cleaning', 'Home Cleaning'),
        ('deep_cleaning', 'Deep Cleaning'),
        ('pest_control', 'Pest Control'),
        ('post_construction', 'Post Construction Cleaning'),
        ('office_commercial', 'Office & Commercial'),
    ]

    name = models.CharField(max_length=100)
    start_price = models.IntegerField(null=True, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    hero_title = models.CharField(max_length=200, blank=True)
    sub_hero_title = models.CharField(max_length=200, blank=True, null=True)
    hero_description = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to='services/', null=True, blank=True)

    def __str__(self):
        return self.name


class ServiceFeature(BaseModel):
    service = models.ForeignKey(Service, related_name='features', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"


class ServiceContent(BaseModel):
    service = models.ForeignKey(Service, related_name='contents', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"


class ServiceRating(BaseModel):
    service = models.ForeignKey(Service, related_name='ratings', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"


class Package(BaseModel):
    PACKAGE_TYPES = [
        ('studio', 'Studio'),
        ('2bhk', '2 BHK'),
        ('villa', 'Villa'),
        ('office', 'Office'),
        ('custom', 'Custom'),
    ]

    service = models.ForeignKey(Service, related_name='packages', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    square_feet = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return f"{self.service.name} - {self.name}"


class AddonCategory(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Addon Categories"

    def __str__(self):
        return self.name


class Addon(BaseModel):
    service = models.ForeignKey(Service, related_name='addons', on_delete=models.CASCADE)
    category = models.ForeignKey(AddonCategory, related_name='addons', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"


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
