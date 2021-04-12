from rest_framework import serializers
from .models import NormalShip, WasteShip, NormalImage, WasteImage
from Accounts.models import Account


class NormalShipSerializer(serializers.HyperlinkedModelSerializer):
    register = serializers.SlugRelatedField(read_only=True,
                                            many=False,
                                            slug_field='srvno')

    class Meta:
        model = NormalShip
        fields = ('id', 'name', 'port', 'code', 'tons', 'types', 'main_img',
                  'is_vpass', 'is_ais', 'is_vhf', 'is_ff', 'img_cnt', 'size',
                  'is_train', 'regit_date', 'region', 'lat', 'lon', 'register',
                  'main_img_id',)


class NormalShipUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NormalShip
        fields = '__all__'


class NormalImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NormalImage
        fields = ('id', 'img', 'regit_date')


class NormalLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NormalShip
        fields = ('id', 'lat', 'lon', 'name', 'regit_date')


class WasteShipSerializer(serializers.HyperlinkedModelSerializer):
    register = serializers.SlugRelatedField(read_only=True,
                                            many=False,
                                            slug_field='srvno')

    class Meta:
        model = WasteShip
        fields = ('id', 'info', 'types', 'lat', 'lon', 'main_img',
                  'is_train', 'regit_date', 'register', 'region', 'img_cnt',
                  'main_img_id')


class WasteShipUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteShip
        fields = '__all__'


class WasteImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteImage
        fields = ('id', 'img', 'regit_date')


class WasteLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteShip
        fields = ('id', 'lat', 'lon', 'info', 'regit_date')
