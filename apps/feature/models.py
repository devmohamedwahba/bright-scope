from django.db import models


class Feature(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    alias = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="fa-solid fa-star"
    )
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if self.order is None:  # only set if not provided
            last_order = Feature.objects.aggregate(models.Max("order"))["order__max"] or 0
            self.order = last_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
