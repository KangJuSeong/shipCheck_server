from django.db import models
from django.utils.html import mark_safe


class Boat(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    imo = models.CharField(unique=True, max_length=255, null=True, blank=True)
    calsign = models.CharField(max_length=255, null=True, blank=True)
    mmsi = models.CharField(max_length=255, null=True, blank=True)
    vessel_type = models.CharField(max_length=255, null=True, blank=True)
    build_year = models.CharField(max_length=255, null=True, blank=True)
    current_flag = models.CharField(max_length=255, null=True, blank=True)
    home_port = models.CharField(max_length=255, null=True, blank=True)
    main_img = models.ImageField(upload_to='boat_img/', null=True, blank=True)
    is_learning = models.BooleanField(default=False)


class WasteBoat(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    detail = models.CharField(max_length=255, null=True, blank=True)
    wasted_img = models.ImageField(upload_to='wasted_img/', null=True, blank=True)
    is_learning = models.BooleanField(default=False)
