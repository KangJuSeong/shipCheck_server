from rest_framework import serializers
from Boats.models import Boat, WasteBoat
import base64
from django.core.files.base import ContentFile


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