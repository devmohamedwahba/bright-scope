from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = [
        ("INITIATED", "Initiated"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    order_id = models.CharField(max_length=100, db_index=True)
    transaction_reference = models.CharField(max_length=100, blank=True, null=True, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='AED')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INITIATED')
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_id} - {self.status}"
