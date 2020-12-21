from django.db import models
from django.utils.html import mark_safe


class Boat(models.Model):
    STATUS_CHOICE = (
        ('NEW', '신상품'), ('USED', '중고')
    )

    title = models.CharField(max_length=100, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    reserve = models.CharField(max_length=100, null=True, blank=True)
    product_status = models.CharField(max_length=4, choices=STATUS_CHOICE,
                                      null=True, blank=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    model_code = models.CharField(max_length=100, null=True, blank=True)
    boat_img = models.ImageField(null=True, blank=True)

    @property
    def thumbnail_preview(self):
        if self.boat_img:
            return mark_safe('<img src="{}" width="300" height="300" />'
                             .format(self.boat_img.url))
        return ""


class WasteBoat(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
