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


logger = logging.getLogger(__name__)


class DetailNormalShipAPI(APIView):
    def get(self, request, pk=None):
        try:
            queryset = NormalShip.objects.get(id=pk)
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
            page_size = 10
            if query_size % page_size == 0:
                count = int(query_size / page_size)
            else:
                count = int(query_size / page_size) + 1
            if page is 1:
                queryset = NormalShip.objects.all()[0:page_size]
            elif page is count:
                start = page_size * (page - 1)
                queryset = NormalShip.objects.all()[start:]
            else:
                start = page_size * (page - 1)
                end = start + page_size
                queryset = NormalShip.objects.all()[start:end]
            serializer = NormalShipSerializer(queryset, many=True)
            data = change_datetime(serializer.data)
            result = {"count": count, "data": data}
            logger.debug('Request List Success : {0} (군번 : {1}, 데이터 : {2})'.format('일반 선박 목록 요청 성공',
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


class DetailWasteShipAPI(APIView):
    def get(self, request, pk=None):
        try:
            queryset = WasteShip.objects.get(id=pk)
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
            page_size = 10
            if query_size % page_size == 0:
                count = int(query_size / page_size)
            else:
                count = int(query_size / page_size) + 1
            if page is 1:
                queryset = WasteShip.objects.all()[0:page_size]
            elif page is count:
                start = page_size * (page - 1)
                queryset = WasteShip.objects.all()[start:]
            else:
                start = page_size * (page - 1)
                end = start + page_size
                queryset = WasteShip.objects.all()[start:end]
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
            logger.debug('Request Location Fail : {0} (군번 : {1}, 오류 내용 : {2})'.format('유기 선박 위치 요청 실패, 유효하지 않은 데이터',
                                                                                      request.user.srvno,
                                                                                      e))
            return self.fail(message='fail')


class ListNormalImageAPI(APIView):
    def get(self, request, pk=None):
        try:
            queryset = NormalShip.objects.get(id=pk)
            img_queryset = NormalImage.objects.filter(n_name=queryset.id)
            serializer = NormalImageSerializer(img_queryset, many=True)
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
            image = NormalImage.objects.get(id=request.data['id'])
            logger.debug('Request Delete Success : {0} (군번 : {1}, 삭제 이미지 : {2})'.format('일반 선박 이미지 삭제 요청 성공',
                                                                                        request.user.srvno,
                                                                                        image))
            image.n_name.img_cnt = image.n_name.img_cnt - 1
            if image.n_name.img_cnt == 0:
                image.n_name.main_img = '/media/NoImage.jpg'
            if image.n_name.main_img == str(image.img):
                image.n_name.main_img = str(NormalImage.objects.filter(n_name=image.n_name)[0])
            image.n_name.save()
            image.delete()
            return self.success(message='success')
        except Exception as e:
            logger.debug('Request Delete Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '일반 선박 이미지 삭제 요청 실패',
                request.user.srvno,
                e,
                request.data))
            return self.fail(message='fail')


class ListWasteImageAPI(APIView):
    def get(self, request, pk=None):
        try:
            queryset = WasteImage.objects.get(id=pk)
            img_queryset = WasteImage.objects.filter(w_id=queryset.id)
            serializer = WasteImageSerializer(img_queryset, many=True)
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
                '유기 선박 이미지 추가 요청 실패, 유효하지 않은 데이터 ',
                request.user.srvno,
                e,
                request.data))
            return self.fail(message='fail')

    def delete(self, request):
        try:
            image = WasteImage.objects.get(id=request.data['id'])
            logger.debug('Request Delete Success : {0} (군번 : {1}, 삭제 이미지 : {2})'.format('유기 선박 이미지 삭제 요청 성공',
                                                                                        request.user.srvno,
                                                                                        image))
            image.w_id.img_cnt = image.w_id.img_cnt - 1
            if image.w_id.img_cnt == 0:
                image.w_id.main_img = '/media/NoImage.jpg'
            if image.w_id.main_img == str(image):
                image.w_id.main_img = str(WasteImage.objects.filter(w_id=image.w_id)[0])
            image.w_id.save()
            image.delete()
            return self.success(message='success')
        except Exception as e:
            logger.debug('Request Delete Fail : {0} (군번 : {1}, 오류 내용 : {2}, 데이터 : {3})'.format(
                '유기 선박 이미지 삭제 요청 실패',
                request.user.srvno,
                e,
                request.data))
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
            if result_set['first'][0][0] is 'n':
                first_ship = NormalShip.objects.get(id=int(result_set['first'][0][2:]))
                first_serial = NormalShipSerializer(first_ship)
                kinds.append(1)
            else:
                first_ship = WasteShip.objects.get(id=int(result_set['first'][0][2:]))
                first_serial = WasteShipSerializer(first_ship)
                kinds.append(0)
            if result_set['second'][0][0] is 'n':
                second_ship = NormalShip.objects.get(id=int(result_set['second'][0][2:]))
                second_serial = NormalShipSerializer(second_ship)
                kinds.append(1)
            else:
                second_ship = WasteShip.objects.get(id=int(result_set['second'][0][2:]))
                second_serial = WasteShipSerializer(second_ship)
                kinds.append(0)
            if result_set['third'][0][0] is 'n':
                third_ship = NormalShip.objects.get(id=int(result_set['third'][0][2:]))
                third_serial = NormalShipSerializer(third_ship)
                kinds.append(1)
            else:
                third_ship = WasteShip.objects.get(id=int(result_set['third'][0][2:]))
                third_serial = WasteShipSerializer(third_ship)
                kinds.append(0)
            first_serial = change_datetime(first_serial.data)
            second_serial = change_datetime(second_serial.data)
            third_serial = change_datetime(third_serial.data)
            result_ship = [first_serial, second_serial, third_serial]
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
