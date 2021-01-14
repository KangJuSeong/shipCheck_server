from django.db import models
from django.utils.html import mark_safe

# id, s_name, s_port, s_code, s_tons, s_type, isVpass, isAis, isVhf, isFf, img_cnt (선박 정보)
# s_id(fk), srvno(fk), s_date, s_img, lat, lon (선박 이미지) 
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

# w_id, w_point, lat, lon, isLearning, img_cnt, img_main
# img_id, w_id, srvno, w_date, w_img, lat, lon (유기/폐 선박 이미지)
class WasteBoat(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    detail = models.CharField(max_length=255, null=True, blank=True)
    wasted_img = models.ImageField(upload_to='wasted_img/', null=True, blank=True)
    is_learning = models.BooleanField(default=False)
