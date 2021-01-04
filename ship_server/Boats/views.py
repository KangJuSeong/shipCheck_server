from utils.custom_view import APIView
from Boats.models import Boat, WasteBoat
from Boats.serializers import BoatSerializer, WasteBoatSerializer
import base64
from django.core.files.base import ContentFile
from keras_model import snippets
from PIL import Image
import io
from utils.best_three import bestThree
# from utils.test_crawling import parse_data
# from django.core.files import File
# import requests
# import random


class DetailBoatAPI(APIView):
    def post(self, request):
        data = Boat.objects.get(id=request.data['id'])
        serializer = BoatSerializer(data)
        return self.success(serializer.data, message='success')


class RegistBoatAPI(APIView):
    def post(self, request):
        if request.data['flag'] == 'Normal':
            serializer = BoatSerializer(data=request.data)
            if not serializer.is_valid(raise_exception=True):
                return self.fail(message="Request Body Error.")
            image_data = base64.b64decode(request.data['image_data'])
            imo = serializer.validated_data['imo']
            serializer.validated_data['main_img'] = ContentFile(image_data,
                                                                imo+'.jpg')
            serializer.save()
            return self.success(message='success')
        elif request.data['flag'] == 'Wasted':
            serializer = WasteBoatSerializer(data=request.data)
            if not serializer.is_valid(raise_exception=True):
                return self.fail(message="Request Body Error")
            image_data = base64.b64decode(request.data['image_data'])
            title = serializer.validated_data['title']
            serializer.validated_data['wasted_img'] = ContentFile(image_data,
                                                                  title+'.jpg')
            serializer.save()
            return self.success(message='success')


class SearchingBoatAPI(APIView):
    def post(self, request):
        data = Boat.objects.all()
        for key, value in request.data.items():
            if value != '':
                if key == 'name':
                    data = data.filter(name__contains=value)
                elif key == 'imo':
                    data = data.filter(imo__contains=value)
                elif key == 'calsign':
                    data = data.filter(calsign__contains=value)
                elif key == 'mmsi':
                    data = data.filter(mmsi__contains=value)
                elif key == 'vessel_type':
                    data = data.filter(vessel_type__contains=value)
                elif key == 'build_year':
                    data = data.filter(build_year__contains=value)
                elif key == 'current_flag':
                    data = data.filter(current_flag__contains=value)
                elif key == 'home_port':
                    data = data.filter(home_port__contains=value)
        searching_data = BoatSerializer(data, many=True)
        if not len(searching_data.data):
            return self.fail(message='DoesNotExist')
        return self.success(data=searching_data.data, message='success')


class WasteBoatAPI(APIView):
    def post(self, request):
        data = WasteBoat.objects.all()
        serializer = WasteBoatSerializer(data, many=True)
        return self.success(data=serializer.data, message='success')


class WasteDetailBoatAPI(APIView):
    def post(self, request):
        pk = request.data['id']
        data = WasteBoat.objects.get(id=pk)
        serializer = WasteBoatSerializer(data)
        return self.success(data=serializer.data, message='success')


class PredictBoat(APIView):
    def post(self, request):
        image_data = base64.b64decode(request.data['image_data'])
        img = Image.open(io.BytesIO(image_data))
        pred = snippets.ai_module(img)
        data = bestThree(pred[0])
        print(data)
        return self.success(data={"hello": "hello"}, message='success')


class test(APIView):
    def post(self, request):
        return self.success(message='success')