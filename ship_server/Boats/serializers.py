from rest_framework import serializers
from .models import Boat, WasteBoat, BoatImg


class BoatImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BoatImg
        fields = ('id', 'img', 'lon', 'lat', 'point', 'add_date')


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


class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    images = BoatImageSerializer(many=True, read_only=True)

    class Meta:
        model = Boat
        fields = ('name', 'images')


class WasteBoatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteBoat
        fields = ('id', 'title', 'latitude', 'longitude', 'detail', 'wasted_img')