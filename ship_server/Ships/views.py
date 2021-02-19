from utils.custom_view import APIView
from .models import NormalShip, NormalImage, WasteShip, WasteImage
from Accounts.models import Account
from .serializers import NormalShipSerializer, NormalImageSerializer, WasteShipSerializer, WasteImageSerializer
from django.core.exceptions import ObjectDoesNotExist
import numpy as np
from django.core.files import File
import base64
from django.core.files.base import ContentFile
from keras_model import snippets
from PIL import Image
from io import BytesIO
import uuid
import io
from utils.best_three import bestThree
from django.db.models import Q
from rest_framework.permissions import AllowAny
import pandas as pd
from datetime import datetime


class DetailNormalShipAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        try:
            queryset = NormalShip.objects.get(id=pk)
            serializer = NormalShipSerializer(queryset)
            return self.success(data=serializer.data, message='success')
        except ObjectDoesNotExist:
            return self.fail(message='Not Exist')

    def delete(self, request, pk=None):
        try:
            queryset = NormalShip.objects.get(id=pk)
            queryset.delete()
            return self.success(message='success')
        except ObjectDoesNotExist:
            return self.fail(message='Not Exist')


class CreateNormalShipAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        status = 0
        status = NormalShip.create_normal_ship(request.data, Account.objects.get(srvno='ADMIN'))
        if not status == 0:
            return self.success(message='success '+str(status))
        else:
            return self.fail(message='Fail Create2')


class ListNormalShipAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class SearchNormalShipAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class DetailWasteShipAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class CreateWasteShipAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class ListWasteShipAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class SearchWasteShipAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class DetailNoramlImageAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class CreateNormalImageAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class DetailWasteImageAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class NormalShipRegister(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        ship_csv = pd.read_csv('D:/기존 사용 DB/선박.csv')
        img_csv = pd.read_csv('D:/기존 사용 DB/선박이미지.csv')
        black = [15]
        for ship_id in ship_csv['id']:
            if ship_id in black:
                continue
            search_row = ship_csv.loc[(ship_csv['id'] == ship_id)]
            name = list(search_row['ship_name'])[0]
            code = list(search_row['registerd_ship_num'])[0]
            size = list(search_row['width_length'])[0]
            weight = list(search_row['weight'])[0]
            find_row = img_csv.loc[(img_csv['shipdb_id'] == ship_id)]  # 필터링 된 row를 이용하여 img 주소 찾기
            img_len = len(list(find_row['ship_image']))
            weight_list = ['톤', 'T', 'ton', 't']
            size_list = ['길이', ',', '폭', ]
            if name == 'none':
                name = '정보 없음'
            if code == 'none':
                code = '정보 없음'
            if size == 'none':
                size = '정보 없음'
            if weight == 'none':
                weight = '정보 없음'
            if not img_len == 0:
                img_path = list(find_row['ship_image'])[0]
                img = Image.open('D:/기존 사용 DB/media/' + img_path)
                img_name = str(uuid.uuid4())
                buf = BytesIO()
                img.save(buf, 'jpeg')
                buf.seek(0)
                img_bytes = buf.read()
                buf.close()
                ship = NormalShip.objects.create(name=name,
                                                 code=code,
                                                 size=size,
                                                 tons=weight,
                                                 img_cnt=img_len,
                                                 register=Account.objects.get(srvno='ADMIN'),
                                                 main_img=ContentFile(img_bytes, str(datetime.today())+img_name+'.jpg'))
                ship.save()
                print('{} 선박 등록 완료'.format(ship_id))
            else:
                ship = NormalShip.objects.create(name=name,
                                                 code=code,
                                                 size=size,
                                                 tons=weight,
                                                 img_cnt=img_len,
                                                 register=Account.objects.get(srvno='ADMIN'))
                ship.save()
                print('{} 선박 등록 완료'.format(ship_id))
        return self.success(message='success')


class WasteShipReigster(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        ship_csv = pd.read_csv('D:/기존 사용 DB/유기,폐 선박.csv')
        img_csv = pd.read_csv('D:/기존 사용 DB/유기,폐 선박 이미지.csv')
        for ship_id in ship_csv['id']:
            search_row = ship_csv.loc[(ship_csv['id'] == ship_id)]
            lat = list(search_row['lat'])[0]
            if lat == 'none':
                lat = 0
            lon = list(search_row['long'])[0]
            if lon == 'none':
                lon = 0
            info = list(search_row['info'])[0]
            info = str(info)
            find_row = img_csv.loc[(img_csv['shipdb_id'] == int(ship_id))]  # 필터링 된 row를 이용하여 img 주소 찾기
            img_len = len(list(find_row['ship_image']))
            if not img_len == 0:
                img_path = list(find_row['ship_image'])[0]
                img = Image.open('D:/기존 사용 DB/media/' + img_path)
                img_name = str(uuid.uuid4())
                buf = BytesIO()
                img.save(buf, 'jpeg')
                buf.seek(0)
                img_bytes = buf.read()
                buf.close()
                ship = WasteShip.objects.create(lat=lat,
                                                lon=lon,
                                                info=info,
                                                img_cnt=img_len,
                                                register=Account.objects.get(srvno='ADMIN'),
                                                main_img=ContentFile(img_bytes, str(datetime.today())+img_name+'.jpg'))
                ship.save()
                print('이미지가 잘 들어갔어요!')
                print('{} 선박 등록 완료'.format(ship_id))
            else:
                ship = WasteShip.objects.create(lat=lat,
                                                lon=lon,
                                                info=info,
                                                img_cnt=img_len,
                                                register=Account.objects.get(srvno='ADMIN'),)
                ship.save()
                print('이미지가 없어요 ㅜㅜ')
                print('{} 선박 등록 완료'.format(ship_id))
        return self.success(message='success')


class NormalImageExtraRegit(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        ship_csv = pd.read_csv('D:/기존 사용 DB/선박.csv')
        img_csv = pd.read_csv('D:/기존 사용 DB/선박이미지.csv')
        for ship_id in ship_csv['id']:
            find_row = img_csv.loc[(img_csv['shipdb_id'] == int(ship_id))]  # 필터링 된 row를 이용하여 img 주소 찾기
            img_len = len(list(find_row['ship_image']))

        return self.success(message='success')


class WasteImageExtraRegit(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return self.success(message='success')


class AllDelete(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        ships = NormalShip.objects.all()
        ships.delete()
        return self.success(message='success')