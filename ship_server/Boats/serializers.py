from rest_framework import serializers
from Boats.models import Boat, WasteBoat
import base64
from django.core.files.base import ContentFile


# class BoatRegistSerializer(serializers.Serializer):
#     flag = serializers.CharField(max_length=255)
#     name = serializers.CharField(max_length=255)
#     imo = serializers.CharField(max_length=255)
#     calsign = serializers.CharField(max_length=255)
#     mmsi = serializers.CharField(max_length=255)
#     vessel_type = serializers.CharField(max_length=255)
#     build_year = serializers.CharField(max_length=255)
#     current_flag = serializers.CharField(max_length=255)
#     home_port = serializers.CharField(max_length=255)
#     image_data = serializers.CharField(max_length=255)

#     def validate(self, data):
#         flag = data.get("flag", None)
#         if flag == 'Normal':
#             print('hello')
#             name = data.get("name", None)
#             imo = data.get("imo", None)
#             calsign = data.get("calsign", None)
#             mmsi = data.get("mmsi", None)
#             vessel_type = data.get("vessel_type", None)
#             build_year = data.get("build_year", None)
#             current_flag = data.get("current_flag", None)
#             home_port = data.get("home_port", None)
#             image_data = data.get("image_data", None)
#             boat = Boat.objects.create(name=name,
#                                        imo=imo,
#                                        calsign=calsign,
#                                        mmsi=mmsi,
#                                        vessel_type=vessel_type,
#                                        build_year=build_year,
#                                        current_flag=current_flag,
#                                        home_port=home_port)
#             image_data = base64.b64decode(image_data)
#             boat.main_img = ContentFile(image_data, 'test' + '.jpg')
#             boat.save()
#             return {
#                 'message': 'Success Regist',
#             }


class BoatSearchingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Boat
        fields = ('id', 'name', 'imo', 'mmsi')


class BoatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Boat
        fields = ('id', 'name', 'imo', 'calsign', 'mmsi', 'vessel_type',
                  'build_year', 'current_flag', 'home_port', 'main_img',
                  'is_learning')


class WasteBoatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteBoat
        fields = ('id', 'title', 'latitude', 'longitude', 'detail', 'wasted_img')