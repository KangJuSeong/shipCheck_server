from utils.custom_view import APIView
from Boats.models import Boat, WasteBoat
from Boats.serializers import BoatSerializer, BoatDetailSerializer, WasteBoatSerializer
# from utils.test_crawling import parse_data


class GetDetailBoatAPI(APIView):
    def post(self, request):
        pk = request.data['id']
        data = Boat.objects.get(id=pk)
        serializer = BoatDetailSerializer(data)
        return self.success(serializer.data, message='success')


class GetSearchingBoatAPI(APIView):
    def post(self, request):
        data = Boat.objects.all()
        for k, v in request.data.items():
            if v != '':
                if k == 'title':
                    data = data.filter(title__contains=v)
                elif k == 'price':
                    data = data.filter(price__contains=v)
                elif k == 'reserve':
                    data = data.filter(reserve__contains=v)
                elif k == 'product_status':
                    data = data.filter(product_status__contains=v)
                elif k == 'manufacturer':
                    data = data.filter(manufacturer__contains=v)
                elif k == 'brand':
                    data = data.filter(brnad__contains=v)
                elif k == 'model_code':
                    data = data.filter(model_code__contains=v)
        searching_data = BoatSerializer(data, many=True)
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
# class test(APIView):
#     def post(self, request):
#         parse_data("005930")
#         return self.success(message='success')