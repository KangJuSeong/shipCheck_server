from django.db import models
from Accounts.models import Account


#  항구를 선택할것인가? 지역 선택? 선박 유형 선택? 등록 날짜, 등록자
class NormalShip(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True)
    port = models.CharField(max_length=10, null=True, blank=True)
    code = models.CharField(max_length=20, null=True, blank=True)
    tons = models.FloatField(default=0)
    types = models.CharField(max_length=10, null=True, blank=True)
    is_vpass = models.BooleanField(default=False)
    is_ais = models.BooleanField(default=False)
    is_vhf = models.BooleanField(default=False)
    is_ff = models.BooleanField(default=False)
    img_cnt = models.IntegerField(default=0)
    main_img = models.ImageField(upload_to='normal_img/',
                                 null=True,
                                 blank=True)
    is_train = models.BooleanField(default=False)
    register = models.ForeignKey(Account, related_name='normal_register',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    regit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.n_name


class NormalImage(models.Model):
    n_name = models.ForeignKey('NormalShip', related_name='normal_ship',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    register = models.ForeignKey(Account, related_name='noraml_add_register',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    img = models.ImageField(upload_to='normal_add_img/',
                            null=True,
                            blank=True)
    regit_date = models.DateTimeField(auto_now_add=True)
    # lat = models.FloatField(default=0)
    # lon = models.FloatField(default=0)


class WasteShip(models.Model):
    point = models.TextField(null=True, blank=True)
    types = models.CharField(max_length=10, null=True, blank=True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    img_cnt = models.IntegerField(default=0)
    is_train = models.BooleanField(default=False)
    regit_date = models.DateTimeField(auto_now_add=True)
    register = models.ForeignKey(Account, related_name='waste_register',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    main_img = models.ImageField(upload_to='waste_img/',
                                 null=True,
                                 blank=True)


class WasteImage(models.Model):
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    regit_date = models.DateTimeField(auto_now_add=True)
    w_id = models.ForeignKey('WasteShip', related_name='waste_ship',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    register = models.ForeignKey(Account, related_name='waste_add_register',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    img = models.ImageField(upload_to='waste_add_img/',
                            null=True,
                            blank=True)