from utils.custom_view import APIView
from .models import NormalShip, NormalImage, WasteShip, WasteImage
from Accounts.models import Account
from .serializers import (NormalShipSerializer, NormalImageSerializer, WasteShipSerializer,
                          WasteImageSerializer, WasteLocationSerializer,
                          NormalShipUpdateSerializer, WasteShipUpdateSerializer)
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
from rest_framework.permissions import AllowAny
import pandas as pd
from datetime import datetime
import time


class DetailNormalShipAPI(APIView):
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

    def put(self, request, pk=None):
        queryset = NormalShip.objects.get(id=pk)
        serializer = NormalShipUpdateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success(message='success')
        return self.fail(message='fail')


class CreateNormalShipAPI(APIView):
    def post(self, request):
        ship_id = NormalShip.create_normal_ship(data=request.data, user=request.user)
        if len(request.data['image_data']) > 1:
            NormalImage.create_normal_image(img_list=request.data['image_data'],
                                            ship_id=ship_id)
        return self.success(message='success')


class ListNormalShipAPI(APIView):
    def get(self, request):
        query_size = NormalShip.objects.count()
        page_size = 50
        count = int(query_size / page_size) + 1
        page = int(request.GET.get('page'))
        if page is 1:
            queryset = NormalShip.objects.all()[0:page_size-1]
        elif page is count:
            start = page_size * (page - 1)
            queryset = NormalShip.objects.all()[start:]
        else:
            start = page_size * (page - 1)
            end = start + page_size
            queryset = NormalShip.objects.all()[start:end]
        serializer = NormalShipSerializer(queryset, many=True)
        result = {'count': count, "data": serializer.data}
        return self.success(data=result, message='success')


class SearchNormalShipAPI(APIView):
    def post(self, request):
        result = NormalShip.searching_normal_ship(data=request.data)
        serializer = NormalShipSerializer(result, many=True)
        return self.success(data=serializer.data, message='success')


class DetailWasteShipAPI(APIView):
    def get(self, request, pk=None):
        try:
            queryset = WasteShip.objects.get(id=pk)
            serializer = WasteShipSerializer(queryset)
            return self.success(data=serializer.data, message='success')
        except ObjectDoesNotExist:
            return self.fail(message='Not Exist')

    def delete(self, request, pk=None):
        try:
            queryset = WasteShip.objects.get(id=pk)
            queryset.delete()
            return self.success(message='success')
        except ObjectDoesNotExist:
            return self.fail(message='Not Exist')

    def put(self, request, pk=None):
        queryset = WasteShip.objects.get(id=pk)
        serializer = WasteShipUpdateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success(message='success')
        return self.fail(message='fail')


class CreateWasteShipAPI(APIView):
    def post(self, request):
        ship_id = WasteShip.create_normal_ship(data=request.data, user=request.user)
        if len(request.data['image_data']) > 1:
            NormalImage.create_normal_image(img_list=request.data['image_data'],
                                            ship_id=ship_id)
        return self.success(message='success')


class ListWasteShipAPI(APIView):
    def get(self, request):
        query_size = WasteShip.objects.count()
        page_size = 50
        count = int(query_size / page_size) + 1
        page = int(request.GET.get('page'))
        if page is 1:
            queryset = WasteShip.objects.all()[0:page_size - 1]
        elif page is count:
            start = page_size * (page - 1)
            queryset = WasteShip.objects.all()[start:]
        else:
            start = page_size * (page - 1)
            end = start + page_size
            queryset = WasteShip.objects.all()[start:end]
        serializer = WasteShipSerializer(queryset, many=True)
        result = {'count': count, "data": serializer.data}
        return self.success(data=result, message='success')


class LocationWasteShipAPI(APIView):
    def get(self, request):
        queryset = WasteShip.objects.all()
        location = WasteLocationSerializer(queryset, many=True)
        return self.success(data=location.data, message='success')


class SearchWasteShipAPI(APIView):
    def post(self, request):
        return self.success(message='success')


class DetailNormalImageAPI(APIView):
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
            if name == 'none':
                name = '정보 없음'
            if code == 'none':
                code = '정보 없음'
            if size == 'none':
                size = '정보 없음'
            if weight == 'none':
                weight = '정보 없음'
            if not img_len == 0:
                img_path = list(find_row['ship_image'])
                img = Image.open('D:/기존 사용 DB/media/' + img_path[0])
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
                                                 region='정보 없음',
                                                 main_img=ContentFile(img_bytes, str(datetime.today())+img_name+'.jpg'))
                ship.save()
                if img_len > 1:
                    for i in range(img_len):
                        if i == 0:
                            continue
                        else:
                            img = Image.open('D:/기존 사용 DB/media/' + img_path[i])
                            img_name = str(uuid.uuid4())
                            buf = BytesIO()
                            img.save(buf, 'jpeg')
                            buf.seek(0)
                            img_bytes = buf.read()
                            buf.close()
                            ship_img = NormalImage.objects.create(n_name=NormalShip.objects.get(id=ship.id),
                                                                  img=ContentFile(img_bytes,
                                                                                  str(datetime.today())+img_name+'.jpg'))
                            ship_img.save()
                            print('{0} / {1}'.format(i, img_len))
                print('{} 선박 등록 완료'.format(ship_id))
            else:
                ship = NormalShip.objects.create(name=name,
                                                 code=code,
                                                 size=size,
                                                 tons=weight,
                                                 img_cnt=img_len,
                                                 region='정보 없음',
                                                 register=Account.objects.get(srvno='ADMIN'))
                ship.save()
                print('이미지가 없어요 ㅜㅜ')
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
                img_path = list(find_row['ship_image'])
                img = Image.open('D:/기존 사용 DB/media/' + img_path[0])
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
                                                region='정보 없음',
                                                main_img=ContentFile(img_bytes, str(datetime.today())+img_name+'.jpg'))
                ship.save()
                if img_len > 1:
                    for i in range(img_len):
                        if i == 0:
                            continue
                        else:
                            img = Image.open('D:/기존 사용 DB/media/' + img_path[i])
                            img_name = str(uuid.uuid4())
                            buf = BytesIO()
                            img.save(buf, 'jpeg')
                            buf.seek(0)
                            img_bytes = buf.read()
                            buf.close()
                            ship_img = WasteImage.objects.create(w_id=WasteShip.objects.get(id=ship.id),
                                                                 img=ContentFile(img_bytes,
                                                                                 str(datetime.today())+img_name+'.jpg'))
                            ship_img.save()
                            print('{0} / {1}'.format(i, img_len))
                print('{} 선박 등록 완료'.format(ship_id))
            else:
                ship = WasteShip.objects.create(lat=lat,
                                                lon=lon,
                                                info=info,
                                                img_cnt=img_len,
                                                region='정보 없음',
                                                register=Account.objects.get(srvno='ADMIN'),)
                ship.save()
                print('이미지가 없어요 ㅜㅜ')
                print('{} 선박 등록 완료'.format(ship_id))
        return self.success(message='success')


class AllDelete(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        ships = WasteShip.objects.all()
        ships.delete()
        return self.success(message='success')