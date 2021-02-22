from rest_framework import serializers
from .models import NormalShip, WasteShip, NormalImage, WasteImage
from Accounts.models import Account


class NormalShipSerializer(serializers.HyperlinkedModelSerializer):
    register = serializers.SlugRelatedField(read_only=True,
                                            many=False,
                                            slug_field='srvno')
    normal_ship = serializers.StringRelatedField(many=True)
    class Meta:
        model = NormalShip
        fields = ('id', 'main_img', 'name', 'port', 'code', 'tons', 'types',
                  'is_vpass', 'is_ais', 'is_vhf', 'is_ff', 'img_cnt', 'size',
                  'is_train', 'regit_date', 'register', 'normal_ship')


class NormalImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NormalImage
        fields = ('id', 'img', 'regit_date')


class WasteShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteShip
        fields = ('id', 'main_img', 'info', 'types', 'lat', 'lon',
                  'is_train', 'regit_date')


class WasteImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteImage
        fields = ('id', 'img', 'regit_date', 'lat', 'lon')
