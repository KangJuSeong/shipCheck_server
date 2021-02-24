from django.db import models
from Accounts.models import Account
import base64
import uuid
from django.core.files.base import ContentFile
from datetime import datetime
from django.db.models import Q


class RegitInfo(models.Model):
    regit_date = models.DateTimeField(auto_now_add=True)
    register = models.ForeignKey(Account,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,)

    class Meta:
        abstract = True


class RegionInfo(models.Model):
    region = models.CharField(max_length=10, null=True, blank= True)

    class Meta:
        abstract = True


#  항구를 선택할것인가? 지역 선택? 선박 유형 선택? 등록 날짜, 등록자
class NormalShip(RegitInfo, RegionInfo):
    name = models.CharField(max_length=10, null=True, blank=True)
    port = models.CharField(max_length=10, null=True, blank=True)
    code = models.CharField(max_length=20, null=True, blank=True)
    tons = models.CharField(max_length=10, null=True, blank=True)
    types = models.CharField(max_length=10, null=True, blank=True)
    size = models.CharField(max_length=15, null=True, blank=True)
    region = models.CharField(max_length=10, null=True, blank=True)
    is_vpass = models.BooleanField(default=False)
    is_ais = models.BooleanField(default=False)
    is_vhf = models.BooleanField(default=False)
    is_ff = models.BooleanField(default=False)
    img_cnt = models.IntegerField(default=0)
    is_train = models.BooleanField(default=False)
    main_img = models.ImageField(upload_to='normal/new/%Y/%m/%d',
                                 null=True,
                                 blank=True)

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
                                         img_cnt=len(data['image_data']),
                                         register=user)
        if len(data['image_data']) > 0:
            img_name = str(uuid.uuid4())
            image = base64.b64decode(data['image_data'][0])
            ship.main_img = ContentFile(image, str(datetime.today())+img_name+'.jpg')
        ship.save()
        return ship.id

    @staticmethod
    def searching_normal_ship(data):
        name = Q(name__contains=data['name'])
        port = Q(port__contains=data['port'])
        code = Q(code__contains=data['code'])
        tons = Q(tons__contains=data['tons'])
        types = Q(types__contains=data['types'])
        size = Q(size__contains=data['size'])
        region = Q(region__contains=data['region'])
        is_vpass = Q(is_vpass__contains=data['is_vpass'])
        is_ais = Q(is_ais__contains=data['is_ais'])
        is_vhf = Q(is_vhf__contains=data['is_vhf'])
        is_ff = Q(is_ff__contains=data['is_ff'])
        result = NormalShip.objects.filter(name | port | code | tons | types | region
                                           | size | is_vpass | is_ais | is_vhf | is_ff)
        return result


class NormalImage(RegitInfo):
    n_name = models.ForeignKey('NormalShip', related_name='normal_imgs',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    img = models.ImageField(upload_to='normal/exist/%Y/%m/%d',
                            null=True,
                            blank=True)
    # lat = models.FloatField(default=0)
    # lon = models.FloatField(default=0)

    def __str__(self):
        return self.img.url

    @staticmethod
    def create_normal_image(img_list, ship_id):
        del img_list[0]
        for img in img_list:
            img_name = str(uuid.uuid4())
            image = base64.b64decode(img)
            ship_img = NormalImage.objects.create(img=ContentFile(image,
                                                                  str(datetime.today()) + img_name + '.jpg'),
                                                  n_name=NormalShip.objects.get(id=ship_id),
                                                  regit_date=datetime.today())
        ship_img.save()


class WasteShip(RegitInfo, RegionInfo):
    info = models.TextField(null=True, blank=True)
    types = models.CharField(max_length=10, null=True, blank=True)
    region = models.CharField(max_length=10, null=True, blank=True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    img_cnt = models.IntegerField(default=0)
    is_train = models.BooleanField(default=False)
    main_img = models.ImageField(upload_to='waste/new/%Y/%m/%d',
                                 null=True,
                                 blank=True)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def create_waste_ship(data, user):
        ship = WasteShip.objects.create(info=data['info'],
                                        types=data['types'],
                                        lat=data['lat'],
                                        lon=data['lon'],
                                        img_cnt=len(data['image_data']),
                                        register=user)
        img_name = str(uuid.uuid4())
        image = base64.b64decode(data['image_data'][0])
        ship.main_img = ContentFile(image, str(datetime.today()) + img_name + '.jpg')
        ship.save()
        return ship.id

    @staticmethod
    def searching_waste_ship(data):
        info = Q(info__contains=data['info'])
        region = Q(region__contains=data['region'])
        types = Q(types__contains=data['types'])
        result = WasteShip.objects.filter(info | region | types)
        return result


class WasteImage(RegitInfo):
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    w_id = models.ForeignKey('WasteShip', related_name='waste_imgs',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    img = models.ImageField(upload_to='waste/exist/%Y/%m/%d',
                            null=True,
                            blank=True)

    def __str__(self):
        return self.img.url

    @staticmethod
    def create_waste_image(img_list, ship_id):
        del img_list[0]
        for img in img_list:
            img_name = str(uuid.uuid4())
            image = base64.b64decode(img)
            ship_img = NormalImage.objects.create(img=ContentFile(image,
                                                                  str(datetime.today()) + img_name + '.jpg'),
                                                  w_id=WasteShip.objects.get(id=ship_id),
                                                  regit_date=datetime.today())
        ship_img.save()
