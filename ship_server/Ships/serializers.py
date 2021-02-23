from rest_framework import serializers
from .models import NormalShip, WasteShip, NormalImage, WasteImage
from Accounts.models import Account


class NormalShipSerializer(serializers.HyperlinkedModelSerializer):
    register = serializers.SlugRelatedField(read_only=True,
                                            many=False,
                                            slug_field='srvno')
    normal_imgs = serializers.StringRelatedField(many=True)

    class Meta:
        model = NormalShip
        fields = ('id', 'main_img', 'name', 'port', 'code', 'tons', 'types',
                  'is_vpass', 'is_ais', 'is_vhf', 'is_ff', 'img_cnt', 'size',
                  'is_train', 'regit_date', 'register', 'normal_imgs')


class NormalShipUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NormalShip
        fields = '__all__'


class NormalImageSerializer(serializers.HyperlinkedModelSerializer):
    n_name = serializers.SlugRelatedField(read_only=True,
                                          many=False,
                                          slug_field='name')

    class Meta:
        model = NormalImage
        fields = ('id', 'img', 'regit_date', 'n_name')


class WasteShipSerializer(serializers.HyperlinkedModelSerializer):
    register = serializers.SlugRelatedField(read_only=True,
                                            many=False,
                                            slug_field='srvno')
    waste_imgs = serializers.StringRelatedField(many=True)

    class Meta:
        model = WasteShip
        fields = ('id', 'main_img', 'info', 'types', 'lat', 'lon',
                  'is_train', 'regit_date', 'register', 'waste_imgs')


class WasteShipUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteShip
        fields = '__all__'


class WasteImageSerializer(serializers.HyperlinkedModelSerializer):
    w_id = serializers.SlugRelatedField(read_only=True,
                                        many=False,
                                        slug_field='id')

    class Meta:
        model = WasteImage
        fields = ('id', 'img', 'regit_date', 'lat', 'lon', 'w_id')


class WasteLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteShip
        fields = ('id', 'lat', 'lon', 'info')
