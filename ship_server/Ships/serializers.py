from rest_framework import serializers
from .models import NormalShip, WasteShip, NormalImage, WasteImage


class NormalShipSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = NormalShip
        fields = ('id', 'main_img', 'name', 'port', 'code', 'tons', 'types',
                  'is_vpass', 'is_ais', 'is_vhf', 'is_ff', 'img_cnt',
                  'is_train', 'regit_date')
        lookup_field = ('register')


class NormalImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NormalImage
        fields = ('id', 'img', 'regit_date')


class WasteShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteShip
        fields = ('id', 'main_img', 'point', 'types', 'lat', 'lon',
                  'is_train', 'regit_date', 'register')


class WasteImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteImage
        fields = ('id', 'img', 'regit_date', 'lat', 'lon')