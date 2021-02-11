from django.db import models


#  항구를 선택할것인가? 지역 선택? 선박 유형 선택?
class NormalShip(models.Model):
    n_name = models.CharField(max_length=10, null=True, blank=True)
    n_port = models.CharField(max_length=10, null=True, balnk=True)
    n_code = models.CharField(max_length=20, null=True, blank=True)
    n_tons = models.FloatField(default=0)
    n_type = models.CharField(max_length=10, null=True, balnk=True)
    is_vpass = models.BooleanField(default=False)
    is_ais = models.BooleanField(default=False)
    is_vhf = models.BooleanField(default=False)
    is_ff = models.BooleanField(default=False)
    img_cnt = models.IntegerField(default=0)
    img_main = models.ImageField(upload_to='boat_img/', null=True, blank=True)
    is_train = models.BooleanField(default=False)


class NormalImage(models.Model):


class WasteShip(models.Model):


class WasteImage