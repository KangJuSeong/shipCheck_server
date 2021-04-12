from utils.custom_view import APIView
from .models import NormalShip, NormalImage, WasteShip, WasteImage
from Accounts.models import Account
from .serializers import (NormalShipSerializer, NormalImageSerializer, WasteShipSerializer,
                          WasteImageSerializer, WasteLocationSerializer, NormalLocationSerializer,
                          NormalShipUpdateSerializer, WasteShipUpdateSerializer,)
from django.core.exceptions import ObjectDoesNotExist
import numpy as np
from django.core.files import File
import base64
from django.core.files.base import ContentFile
from keras_model.prediction_ship import ai_module
from PIL import Image
from io import BytesIO
import uuid
import io
from utils.best_three import best_three
from rest_framework.permissions import AllowAny
from datetime import datetime
import time
import os
import csv
import logging
import random
from utils.change_format import change_datetime
from django.db.models import Q


logger = logging.getLogger(__name__)


class DetailNormalShipAPI(APIView):
    def get(self, request, pk=None):
        try:
            queryset = NormalShip.objects.filter(id=pk).select_related('register')[0]
            serializer = NormalShipSerializer(queryset)
            result = change_datetime(data=serializer.data)
            logger.debug('Request Detail Success : {0} (군번 : {1}, 일반 선박 ID : {2})'.format('일반 선박 정보 요청 성공',
                                                                                          request.user.srvno,
                                                                                          pk))
            return self.success(data=result, message='success')
        except Exception as e:
            logger.debug('Request Detail Fail : {0} (군번 : {1}, 일반 선박 ID : {2} 오류 내용 : {3})'.format('일반 선박 정보 요청 실패',
                                                                                                   request.user.srvno,
                                                                                                   pk,
                                                                                                   e))
            return self.fail(message='fail')

    def delete(self, request, pk=None):
        if request.user.user_level >= 2:
            try:
                queryset = NormalShip.objects.get(id=pk)
                logger.debug('Request Delete Success : {0} (군번 : {1}, 일반 선박 데이터 : {2} 선박 이미지 : {3})'.format('일반 선박 제거 요청 성공',
                                                                                                                request.user.srvno,
                                                                                                                queryset,
                                                                                                                NormalImage.objects.filter(n_name=queryset)))
                queryset.delete()
                return self.success(message='success')
            except Exception as e:
                logger.debug('Request Delete Fail : {0} (군번 : {1}, 일반 선박 ID : {2} 오류 내용 : {3})'.format('일반 선박 제거 요청 실패',
                                                                                                       request.user.srvno,
                                                                                                       pk,
                                                                                                       e))
                return self.fail(message='fail')
        else:
            return self.fail(message='No permission')

    def post(self, request, pk=None):
        if request.user.user_level >= 2:
            try:
                queryset = NormalShip.objects.get(id=pk)
                serializer = NormalShipUpdateSerializer(queryset, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    logger.debug('Request Update Success : {0} (군번 : {1}, 데이터 : {2} 일반 선박 ID : {3})'.format('일반 선박 수정 요청 성공',
                                                                                                            request.user.srvno,
                                                                                                            request.data,
                                                                                                            pk))
                return self.success(message='success')
            except Exception as e:
                logger.debug('Request Update Fail : {0} (군번 : {1}, 데이터 : {2} 일반 선박 ID : {3} 오류 내용 : {4})'.format('일반 선박 수정 요청 실패',
                                                                                                                 request.user.srvno,
                                                                                                                 request.data,
                                                                                                                 pk,
                                                                                                                 e))
                return self.fail(message='fail')
        else:
            return self.fail(message='No Permission')


class CreateNormalShipAPI(APIView):
    def post(self, request):
        try:
            ship_id = NormalShip.create_normal_ship(data=request.data, user=request.user)
            logger.debug('Request Create Success : {0} (군번 : {1}, 데이터 : {2})'.format('일반 선박 등록 요청 성공',
                                                                                     request.user.srvno,
                                                                                     request.data))
            return self.success(data={"id": str(ship_id)}, message='success')
        except Exception as e:
            logger.debug('Request Create Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '일반 선박 등록 요청 실패',
                request.user.srvno,
                e,
                request.data))
            return self.fail(message='fail')


class ListNormalShipAPI(APIView):
    def get(self, request):
        page = int(request.GET.get('page'))
        try:
            query_size = NormalShip.objects.count()
            queryset = NormalShip.objects.all().select_related('register')
            page_size = 10
            if query_size % page_size == 0:
                count = int(query_size / page_size)
            else:
                count = int(query_size / page_size) + 1
            if page is 1:
                queryset = queryset[0:page_size]
            elif page is count:
                start = page_size * (page - 1)
                queryset = queryset[start:]
            else:
                start = page_size * (page - 1)
                end = start + page_size
                queryset = queryset[start:end]
            serializer = NormalShipSerializer(queryset, many=True)
            data = change_datetime(serializer.data)
            result = {"count": count, "data": data}
            logger.debug('Request List Success : {0} (군번 : {1}, 페이지 : {2})'.format('일반 선박 목록 요청 성공',
                                                                                   request.user.srvno,
                                                                                   page))
            return self.success(data=result, message='success')
        except Exception as e:
            logger.debug('Request List Fail : {0} (군번 : {1}, 오류내용 : {2})'.format('일반 선박 목록 요청 실패',
                                                                                 request.user.srvno,
                                                                                 e))
            return self.fail(message='fail')


class SearchNormalShipAPI(APIView):
    def post(self, request):
        try:
            queryset = NormalShip.searching_normal_ship(data=request.data)
            query_size = queryset.count()
            page_size = 10
            page = int(request.GET.get('page'))
            if query_size % page_size == 0:
                count = int(query_size / page_size)
            else:
                count = int(query_size / page_size) + 1
            if page is 1:
                queryset = queryset[0:page_size]
            elif page is count:
                start = page_size * (page - 1)
                queryset = queryset[start:]
            else:
                start = page_size * (page - 1)
                end = start + page_size
                queryset = queryset[start:end]
            serializer = NormalShipSerializer(queryset, many=True)
            data = change_datetime(serializer.data)
            result = {'count': count, "data": data}
            logger.debug('Request Search Success : {0} (군번 : {1}, 데이터 : {2})'.format('일반 선박 검색 요청 성공',
                                                                                     request.user.srvno,
                                                                                     request.data))
            return self.success(data=result, message='success')
        except Exception as e:
            logger.debug('Request Search Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '일반 선박 검색 요청 실패',
                request.user.srvno,
                e,
                request.data))
            return self.fail(message='fail')


class LocationNormalShipAPI(APIView):
    def get(self, request):
        try:
            n_queryset = NormalShip.objects.all()
            n_location = NormalLocationSerializer(n_queryset, many=True)
            result = change_datetime(n_location.data)
            logger.debug('Request Location Success : {0} (군번 : {1})'.format('일반 선박 위치 요청 성공', request.user.srvno))
            return self.success(data=result, message='success')
        except Exception as e:
            logger.debug('Request Location Fail : {0} (군번 : {1}, 오류 내용 : {2})'.format('일반 선박 위치 요청 실패',
                                                                                      request.user.srvno,
                                                                                      e))
            return self.fail(message='fail')

    def post(self, request):
        try:
            x, y = float(request.data['lat']), float(request.data['lon'])
            scope = 0.03
            q = Q()
            q.add(Q(lat__lt=x+scope), q.AND)
            q.add(Q(lat__gt=x-scope), q.AND)
            q.add(Q(lon__lt=y+scope), q.AND)
            q.add(Q(lon__gt=y-scope), q.AND)
            queryset = NormalShip.objects.filter(q)
            serializer = NormalLocationSerializer(queryset, many=True)
            logger.debug('Request Location Success : {0} (군번 : {1})'.format('일반 선박 주변 위치 요청 성공', request.user.srvno))
            return self.success(data=serializer.data, message='success')
        except Exception as e:
            logger.debug('Request Location Fail : {0} (군번 : {1}, 오류 내용 : {2})'.format('일반 선박 주변 위치 요청 실패',
                                                                                      request.user.srvno,
                                                                                      e))
            return self.fail(message='fail')


class DetailWasteShipAPI(APIView):
    def get(self, request, pk=None):
        try:
            queryset = WasteShip.objects.filter(id=pk).select_related('register')[0]
            serializer = WasteShipSerializer(queryset)
            result = change_datetime(serializer.data)
            logger.debug('Request Detail Success : {0} (군번 : {1}, 유기 선박 ID : {2})'.format('유기 선박 정보 요청 성공',
                                                                                          request.user.srvno,
                                                                                          pk))
            return self.success(data=result, message='success')
        except Exception as e:
            logger.debug('Request Detail Fail : {0} (군번 : {1}, 유기 선박 ID : {2} 오류 내용 : {3})'.format('유기 선박 정보 요청 실패',
                                                                                                     request.user.srvno,
                                                                                                     pk,
                                                                                                     e))
            return self.fail(message='fail')

    def delete(self, request, pk=None):
        if request.user.user_level >= 2:
            try:
                queryset = WasteShip.objects.get(id=pk)
                logger.debug('Request Delete Success : {0} (군번 : {1}, 일반 선박 데이터 : {2} 선박 이미지 : {3})'.format('유기 선박 제거 요청 성공',
                                                                                                               request.user.srvno,
                                                                                                               queryset,
                                                                                                               WasteImage.objects.filter(w_id=queryset)))
                queryset.delete()
                return self.success(message='success')
            except Exception as e:
                logger.debug('Request Delete Fail : {0} (군번 : {1}, 유기 선박 ID : {2} 오류 내용 : {3})'.format('유기 선박 제거 요청 실패',
                                                                                                       request.user.srvno,
                                                                                                       pk,
                                                                                                       e))
                return self.fail(message='fail')
        else:
            return self.fail(message='No permission')

    def post(self, request, pk=None):
        if request.user.user_level >= 2:
            try:
                queryset = WasteShip.objects.get(id=pk)
                serializer = WasteShipUpdateSerializer(queryset, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    logger.debug('Request Update Success : {0} (군번 : {1}, 데이터 : {2} 유기 선박 ID : {3})'.format('유기 선박 수정 요청 성공',
                                                                                                            request.user.srvno,
                                                                                                            request.data,
                                                                                                            pk))
                    return self.success(message='success')
            except Exception as e:
                logger.debug('Request Update Fail : {0} (군번 : {1}, 데이터 : {2} 유기 선박 ID : {3} 오류 내용 : {4})'.format('유기 선박 수정 요청 실패',
                                                                                                                 request.user.srvno,
                                                                                                                 request.data,
                                                                                                                 pk,
                                                                                                                 e))
                return self.fail(message='fail')
        else:
            return self.fail(message='No permission')


class CreateWasteShipAPI(APIView):
    def post(self, request):
        try:
            ship_id = WasteShip.create_waste_ship(data=request.data, user=request.user)
            logger.debug('Request Create Success : {0} (군번 : {1}, 데이터 : {2})'.format('유기 선박 등록 요청 성공',
                                                                                     request.user.srvno,
                                                                                     request.data))
            return self.success(data={"id": str(ship_id)}, message='success')
        except Exception as e:
            logger.debug('Request Create Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '유기 선박 등록 요청 실패',
                request.user.srvno,
                e,
                request.data))
            return self.fail(message='fail')


class ListWasteShipAPI(APIView):
    def get(self, request):
        page = int(request.GET.get('page'))
        try:
            query_size = WasteShip.objects.count()
            queryset = WasteShip.objects.all().select_related('register')
            page_size = 10
            if query_size % page_size == 0:
                count = int(query_size / page_size)
            else:
                count = int(query_size / page_size) + 1
            if page is 1:
                queryset = queryset[0:page_size]
            elif page is count:
                start = page_size * (page - 1)
                queryset = queryset[start:]
            else:
                start = page_size * (page - 1)
                end = start + page_size
                queryset = queryset[start:end]
            serializer = WasteShipSerializer(queryset, many=True)
            data = change_datetime(serializer.data)
            result = {'count': count, "data": data}
            logger.debug('Request List Success : {0} (군번 : {1}, 데이터 : {2})'.format('유기 선박 목록 요청 성공',
                                                                                   request.user.srvno,
                                                                                   page))
            return self.success(data=result, message='success')
        except Exception as e:
            logger.debug('Request List Fail : {0} (군번 : {1}, 오류 내용 : {2})'.format('유기 선박 목록 요청 실패',
                                                                                  request.user.srvno,
                                                                                  e))
            return self.fail(message='fail')


class SearchWasteShipAPI(APIView):
    def post(self, request):
        try:
            queryset = WasteShip.searching_waste_ship(data=request.data)
            query_size = queryset.count()
            page_size = 10
            page = int(request.GET.get('page'))
            if query_size % page_size == 0:
                count = int(query_size / page_size)
            else:
                count = int(query_size / page_size) + 1
            if page is 1:
                queryset = queryset[0:page_size]
            elif page is count:
                start = page_size * (page - 1)
                queryset = queryset[start:]
            else:
                start = page_size * (page - 1)
                end = start + page_size
                queryset = queryset[start:end]
            serializer = WasteShipSerializer(queryset, many=True)
            data = change_datetime(serializer.data)
            result = {'count': count, "data": data}
            logger.debug('Request Search Success : {0} (군번 : {1}, 데이터 : {2})'.format('유기 선박 검색 요청 성공',
                                                                                     request.user.srvno,
                                                                                     request.data))
            return self.success(data=result, message='success')
        except Exception as e:
            logger.debug('Request Search Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '유기 선박 검색 요청 실패',
                request.user.srvno,
                e,
                request.data))
            return self.fail(message='fail')


class LocationWasteShipAPI(APIView):
    def get(self, request):
        try:
            w_queryset = WasteShip.objects.all()
            w_location = WasteLocationSerializer(w_queryset, many=True)
            result = change_datetime(w_location.data)
            logger.debug('Request Location Success : {0} (군번 : {1})'.format('유기 선박 위치 요청 성공', request.user.srvno))
            return self.success(data=result, message='success')
        except Exception as e:
            logger.debug('Request Location Fail : {0} (군번 : {1}, 오류 내용 : {2})'.format('유기 선박 위치 요청 실패',
                                                                                      request.user.srvno,
                                                                                      e))
            return self.fail(message='fail')

    def post(self, request):
        try:
            x, y = float(request.data['lat']), float(request.data['lon'])
            q = Q()
            scope = 0.03
            q.add(Q(lat__lt=x+scope), q.AND)
            q.add(Q(lat__gt=x-scope), q.AND)
            q.add(Q(lon__lt=y+scope), q.AND)
            q.add(Q(lon__gt=y-scope), q.AND)
            queryset = WasteShip.objects.filter(q)
            serializer = WasteLocationSerializer(queryset, many=True)
            logger.debug('Request Location Success : {0} (군번 : {1})'.format('유기 선박 주변 위치 요청 성공', request.user.srvno))
            return self.success(data=serializer.data, message='success')
        except Exception as e:
            logger.debug('Request Location Fail : {0} (군번 : {1}, 오류 내용 : {2})'.format('유기 선박 주변 위치 요청 실패',
                                                                                      request.user.srvno,
                                                                                      e))
            return self.fail(message='fail')


class ListNormalImageAPI(APIView):
    def get(self, request, pk=None):
        try:
            queryset = NormalImage.objects.filter(n_name=pk)
            serializer = NormalImageSerializer(queryset, many=True)
            logger.debug('Request List Success : {0} (군번 : {1}, 데이터 : {2})'.format('일반 선박 이미지 목록 요청 성공',
                                                                                   request.user.srvno,
                                                                                   pk))
            return self.success(data=serializer.data, message='success')
        except Exception as e:
            logger.debug('Request List Fail : {0} (군번 : {1}, 오류 내용 : {2})'.format('일반 선박 이미지 목록 요청 실패',
                                                                                  request.user.srvno,
                                                                                  e))
            return self.fail(message='fail')


class NormalImageAPI(APIView):
    def post(self, request):
        try:
            NormalImage.create_normal_image(request.FILES['image_data'], request.data['id'], request.user)
            logger.debug('Request Create Success : {0} (군번 : {1}, 데이터 : {2})'.format('일반 선박 이미지 추가 요청 성공',
                                                                                     request.user.srvno,
                                                                                     request.data))
            return self.success(message='success')
        except Exception as e:
            logger.debug('Request Create Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '일반 선박 이미지 추가 요청 실패',
                request.user.srvno,
                e,
                request.data))
            return self.fail(message='fail')

    def delete(self, request):
        try:
            image = NormalImage.objects.get(id=request.GET.get('id'))
            image.n_name.img_cnt = image.n_name.img_cnt - 1
            if image.n_name.img_cnt == 0:
                image.n_name.main_img = '/media/NoImage.jpg'
                image.n_name.main_img_id = -1
            if image.n_name.main_img_id == image.id:
                main = NormalImage.objects.filter(n_name=image.n_name).exclude(id=image.id)[0]
                image.n_name.main_img = str(main)
                image.n_name.main_img_id = main.id
            image.n_name.save()
            image.delete()
            logger.debug('Request Delete Success : {0} (군번 : {1}, 삭제 이미지 : {2})'.format('일반 선박 이미지 삭제 요청 성공',
                                                                                        request.user.srvno,
                                                                                        image))
            return self.success(message='success')
        except Exception as e:
            logger.debug('Request Delete Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '일반 선박 이미지 삭제 요청 실패',
                request.user.srvno,
                e,
                request.GET.get('id')))
            return self.fail(message='fail')


class ChangeNormalMainImage(APIView):
    def post(self, request):
        try:
            image = NormalImage.objects.filter(id=request.data['id'])[0]
            NormalShip.objects.filter(id=image.n_name_id).update(main_img=str(image), main_img_id=image.id)
            logger.debug('Request Update Success : {0} (군번 : {1}, 대표 수정 이미지 : {2})'.format('일반 선박 대표 이지미 수정 요청 성공',
                                                                                           request.user.srvno,
                                                                                           image))
            return self.success(message='success')
        except Exception as e:
            logger.debug('Request Update Fail : {0} (군번 : {1}, 대표 수정 이미지 : {2} 오류 내용 : {3})'.format('일반 선박 대표 이지미 수정 요청 실패',
                                                                                                    request.user.srvno,
                                                                                                    request.data,
                                                                                                    e))
            return self.fail(message='fail')


class ListWasteImageAPI(APIView):
    def get(self, request, pk=None):
        try:
            queryset = WasteImage.objects.filter(w_id=pk)
            serializer = WasteImageSerializer(queryset, many=True)
            logger.debug('Request List Success : {0} (군번 : {1}, 데이터 : {2})'.format('유기 선박 이미지 목록 요청 성공',
                                                                                   request.user.srvno,
                                                                                   pk))
            return self.success(data=serializer.data, message='success')
        except Exception as e:
            logger.debug('Request List Fail : {0} (군번 : {1}, 오류 내용 : {2})'.format('유기 선박 이미지 목록 요청 실패, 유효하지 않은 데이터',
                                                                                  request.user.srvno,
                                                                                  e))
            return self.fail(message='fail')


class WasteImageAPI(APIView):
    def post(self, request):
        try:
            WasteImage.create_waste_image(request.FILES['image_data'], request.data['id'], request.user)
            logger.debug('Request Create Success : {0} (군번 : {1}, 데이터 : {2})'.format('유기 선박 이미지 추가 요청 성공',
                                                                                     request.user.srvno,
                                                                                     request.data))
            return self.success(message='success')
        except Exception as e:
            logger.debug('Request Create Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '유기 선박 이미지 추가 요청 실패',
                request.user.srvno,
                e,
                request.data))
            return self.fail(message='fail')

    def delete(self, request):
        try:
            image = WasteImage.objects.get(id=request.GET.get('id'))
            image.w_id.img_cnt = image.w_id.img_cnt - 1
            if image.w_id.img_cnt == 0:
                image.w_id.main_img = '/media/NoImage.jpg'
                image.w_id.main_img_id = -1
            if image.w_id.main_img_id == image.id:
                main = WasteImage.objects.filter(w_id=image.w_id).exclude(id=image.id)[0]
                image.w_id.main_img = str(main)
                image.w_id.main_img_id = main.id
            image.w_id.save()
            image.delete()
            logger.debug('Request Delete Success : {0} (군번 : {1}, 삭제 이미지 : {2})'.format('유기 선박 이미지 삭제 요청 성공',
                                                                                        request.user.srvno,
                                                                                        image))
            return self.success(message='success')
        except Exception as e:
            logger.debug('Request Delete Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '유기 선박 이미지 삭제 요청 실패',
                request.user.srvno,
                e,
                request.GET.get('id')))
            return self.fail(message='fail')


class ChangeWasteMainImage(APIView):
    def post(self, request):
        try:
            image = WasteImage.objects.filter(id=request.data['id'])[0]
            WasteShip.objects.filter(id=image.w_id_id).update(main_img=str(image), main_img_id=image.id)
            logger.debug('Request Update Success : {0} (군번 : {1}, 대표 수정 이미지 : {2})'.format('유기 선박 대표 이지미 수정 요청 성공',
                                                                                           request.user.srvno,
                                                                                           image))
            return self.success(message='success')
        except Exception as e:
            logger.debug(
                'Request Update Fail : {0} (군번 : {1}, 대표 수정 이미지 : {2} 오류 내용 : {2})'.format('유기 선박 대표 이지미 수정 요청 실패',
                                                                                           request.user.srvno,
                                                                                           request.data,
                                                                                           e))
            return self.fail(message='fail')


class PredictShipAPI(APIView):
    def post(self, request):
        try:
            img = Image.open(request.FILES['image_data'])
            now = datetime.now()
            if not(os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + '/media/predicted_img/' + now.strftime(
                    "%Y/%m/%d"))):
                os.makedirs(os.path.dirname(os.path.realpath(__file__)) + '/media/predicted_img/' + now.strftime(
                    "%Y/%m/%d"))
            img.save(os.path.dirname(os.path.realpath(__file__)) + '/media/predicted_img/' + now.strftime(
                "%Y/%m/%d/%H_%M_%S") + '_' + request.user.srvno + ".jpg")
            data = ai_module(img)
            result_set = best_three(data[0])
            kinds = list()
            result_ship = list()
            seq_list = ['first', 'second', 'third']
            q = Q()
            _q = Q()
            for i in seq_list:
                if result_set[i][0][0] is 'n':
                    q.add(Q(id=int(result_set[i][0][2:])), q.OR)
                    kinds.append(1)
                else:
                    _q.add(Q(id=int(result_set[i][0][2:])), _q.OR)
                    kinds.append(0)
            n_ship = NormalShip.objects.filter(q).select_related('register')
            w_ship = WasteShip.objects.filter(_q).select_related('register')
            n_idx = 0
            w_idx = 0
            for i in kinds:
                if i == 1:
                    serializer = change_datetime(NormalShipSerializer(n_ship[n_idx]).data)
                    result_ship.append(serializer)
                    n_idx += 1
                else:
                    serializer = change_datetime(WasteShipSerializer(w_ship[w_idx]).data)
                    serializer['name'] = serializer['info']
                    result_ship.append(serializer)
                    w_idx += 1
            result = {'result': result_ship, 'kinds': kinds, 'percent': [result_set['first'][1],
                                                                         result_set['second'][1],
                                                                         result_set['third'][1]]}
            log_result = {'1': {'id': result_ship[0]['id'], 'name': result_ship[0]['name'], 'percent': result_set['first'][1], 'kinds': kinds[0]},
                          '2': {'id': result_ship[1]['id'], 'name': result_ship[1]['name'], 'percent': result_set['second'][1], 'kinds': kinds[1]},
                          '3': {'id': result_ship[2]['id'], 'name': result_ship[2]['name'], 'percent': result_set['third'][1], 'kinds': kinds[2]}}
            logger.debug('Request Predict Success : {0} (군번 : {1}, 결과 : {2})'.format('선박 AI 요청 성공',
                                                                                     request.user.srvno,
                                                                                     log_result))
            return self.success(data=result, message='success')
        except Exception as e:
            logger.debug('Request Predict Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '선박 AI 요청 실패',
                request.user.srvno,
                e,
                request.data))
            return self.fail(message='fail')


class Test(APIView):
    def post(self, request):
        x, y = request.data['lat'], request.data['lon']
        q = Q()
        q.add(Q(lat__lt=x+0.03), q.AND)
        q.add(Q(lat__gt=x-0.03), q.AND)
        q.add(Q(lon__lt=y+0.03), q.AND)
        q.add(Q(lon__gt=y-0.03), q.AND)
        queryset = NormalShip.objects.filter(q)
        serializer = NormalLocationSerializer(queryset, many=True)
        return self.success(data=serializer.data, message='success')
