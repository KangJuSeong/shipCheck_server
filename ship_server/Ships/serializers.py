from rest_framework import serializers
from .models import NormalShip, WasteShip, NormalImage, WasteImage, OwnerInfo, NormalTrackingCoordinate, WasteTrackingCoordinate
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
                  'main_img_id', 'register_unit',)


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
                  'main_img_id', 'register_unit',)


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


class OwnerInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OwnerInfo
        fields = ('id', 'own_name', 'phone', 'address', 'registry_date',
                  'agreement_paper', 'own_img', 'privacy_agree',)


class NormalTrackingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NormalTrackingCoordinate
        fields = ('lat', 'lon', 'check_date',)


class WasteTrackingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteTrackingCoordinate
        fields = ('lat', 'lon', 'check_date',)
