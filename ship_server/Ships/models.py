from django.db import models
from Accounts.models import Account
import base64
import uuid
from django.core.files.base import ContentFile
from datetime import datetime
from django.db.models import Q


# class OwnerInfo(models.Model):
#     privacy_agree = models.BooleanField(default=False)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     phone = models.CharField(max_length=255, null=True, blank=True)
#     address = models.CharField(max_length=255, null=True, blank=True)
#     agreement_paper = models.ImageField(upload_to='agreement_paper/%Y/%m/%d',
#                                         null=True,
#                                         blank=True)


# class TrackingCoordinate(models.Model):
#     lat = models.FloatField(default=0)
#     lon = models.FloatField(default=0)
#     ship = models.ForeignKey('NormalShip', on_delete=models.CASCADE)


class RegitInfo(models.Model):
    regit_date = models.DateTimeField(auto_now_add=True)
    register = models.ForeignKey(Account,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,)

    class Meta:
        abstract = True


class RegionInfo(models.Model):
    region = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


#  항구를 선택할것인가? 지역 선택? 선박 유형 선택? 등록 날짜, 등록자
class NormalShip(RegitInfo, RegionInfo):
    name = models.CharField(max_length=255, null=True, blank=True)
    port = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    tons = models.CharField(max_length=255, null=True, blank=True)
    types = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    is_vpass = models.BooleanField(default=False)
    is_ais = models.BooleanField(default=False)
    is_vhf = models.BooleanField(default=False)
    is_ff = models.BooleanField(default=False)
    img_cnt = models.IntegerField(default=0)
    is_train = models.BooleanField(default=False)
    register_unit = models.CharField(max_length=255, null=True, blank=True)
    main_img = models.CharField(max_length=255, null=True, blank=True)
    main_img_id = models.IntegerField(default=-1)
    # owner = models.OneToOneField('OwnerInfo', on_delete=models.CASCADE)

    class Meta:
        db_table = 'NormalShip'

    def __str__(self):
        return str(self.id)

    @staticmethod
    def create_normal_ship(data, user):
        ship = NormalShip.objects.create(name=data['name'],
                                         port=data['port'],
                                         code=data['code'],
                                         tons=data['tons'],
                                         types=data['types'],
                                         size=data['size'],
                                         is_vpass=data['is_vpass'],
                                         is_ais=data['is_ais'],
                                         is_vhf=data['is_vhf'],
                                         is_ff=data['is_ff'],
                                         register=user,
                                         region=data['region'],
                                         lat=data['lat'],
                                         lon=data['lon'],
                                         main_img='/media/NoImage.jpg')
        return ship.id

    @staticmethod
    def searching_normal_ship(data):
        ships = NormalShip.objects.all().select_related('register')
        if not data['name'] == '':
            ships = ships.filter(name__contains=data['name'])
        if not data['port'] == '':
            ships = ships.filter(port__contains=data['port'])
        if not data['types'] == '':
            ships = ships.filter(types__contains=data['types'])
        if not data['region'] == '':
            ships = ships.filter(region__contains=data['region'])
        if not data['code'] == '':
            ships = ships.filter(code__contains=data['code'])
        if data['is_vpass'] is True:
            ships = ships.filter(is_vpass=True)
        if data['is_ais'] is True:
            ships = ships.filter(is_ais=True)
        if data['is_vhf'] is True:
            ships = ships.filter(is_vhf=True)
        if data['is_ff'] is True:
            ships = ships.filter(is_ff=True)
        return ships


class NormalImage(RegitInfo, RegionInfo):
    n_name = models.ForeignKey('NormalShip', related_name='normal_imgs',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)
    img = models.ImageField(upload_to='normal/exist/%Y/%m/%d',
                            null=True,
                            blank=True)

    class Meta:
        db_table = 'NormalImage'

    def __str__(self):
        return self.img.url

    @staticmethod
    def create_normal_image(image, ship_id, user):
        ship = NormalShip.objects.get(id=ship_id)
        image.name = str(datetime.today()) + str(uuid.uuid4()) + '.jpg'
        ship_img = NormalImage.objects.create(img=image,
                                              n_name=ship,
                                              regit_date=datetime.today(),
                                              register=user)
        ship.img_cnt = ship.img_cnt + 1
        if ship.img_cnt == 1:
            ship.main_img = str(ship_img)
            ship.main_img_id = ship_img.id
        ship.save()


class WasteShip(RegitInfo, RegionInfo):
    info = models.TextField(null=True, blank=True)
    types = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    img_cnt = models.IntegerField(default=0)
    is_train = models.BooleanField(default=False)
    register_unit = models.CharField(max_length=255, null=True, blank=True)
    main_img = models.CharField(max_length=255, null=True, blank=True)
    main_img_id = models.IntegerField(default=-1)

    class Meta:
        db_table = 'WasteShip'

    def __str__(self):
        return str(self.id)

    @staticmethod
    def create_waste_ship(data, user):
        ship = WasteShip.objects.create(info=data['info'],
                                        types=data['types'],
                                        lat=data['lat'],
                                        lon=data['lon'],
                                        region=data['region'],
                                        register=user,
                                        main_img='/media/NoImage.jpg')
        return ship.id

    @staticmethod
    def searching_waste_ship(data):
        ships = WasteShip.objects.all().select_related('register')
        if not data['id'] is '':
            ships = ships.filter(id=data['id'])
            return ships
        if not data['info'] is '':
            ships = ships.filter(info__contains=data['info'])
        if not data['region'] is '':
            ships = ships.filter(region__contains=data['region'])
        if not data['types'] is '':
            ships = ships.filter(types__contains=data['types'])
        return ships


class WasteImage(RegitInfo, RegionInfo):
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    w_id = models.ForeignKey('WasteShip', related_name='waste_imgs',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    img = models.ImageField(upload_to='waste/exist/%Y/%m/%d',
                            null=True,
                            blank=True)

    class Meta:
        db_table = 'WasteImage'

    def __str__(self):
        return self.img.url

    @staticmethod
    def create_waste_image(image, ship_id, user):
        ship = WasteShip.objects.get(id=ship_id)
        image.name = str(datetime.today()) + str(uuid.uuid4()) + '.jpg'
        ship_img = WasteImage.objects.create(img=image,
                                             w_id=ship,
                                             regit_date=datetime.today(),
                                             register=user)
        ship.img_cnt = ship.img_cnt + 1
        if ship.img_cnt == 1:
            ship.main_img = str(ship_img)
            ship.main_img_id = ship_img.id
        ship.save()
        ship_img.save()
