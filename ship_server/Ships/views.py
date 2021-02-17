from utils.custom_view import APIView
from .models import NormalShip, NormalImage, WasteShip, WasteImage
from .serializers import NormalShipSerializer, NormalImageSerializer, WasteShipSerializer, WasteImageSerializer
from django.core.exceptions import ObjectDoesNotExist
import base64
from django.core.files.base import ContentFile
from keras_model import snippets
from PIL import Image
import io
from utils.best_three import bestThree
from django.db.models import Q


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


class CreateNormalShipAPI(APIView):
    def post(self, request):
        status = 0
        status = NormalShip.create_normal_ship(request.data, request.user)
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