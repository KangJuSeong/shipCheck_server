from rest_framework import serializers
from .models import NormalShip, WasteShip, NormalImage, WasteImage
from Accounts.models import Account


class NormalShipSerializer(serializers.HyperlinkedModelSerializer):
    register = serializers.SlugRelatedField(read_only=True,
                                            many=False,
                                            slug_field='srvno')

    class Meta:
        model = NormalShip
        fields = ('id', 'main_img', 'name', 'port', 'code', 'tons', 'types',
                  'is_vpass', 'is_ais', 'is_vhf', 'is_ff', 'img_cnt', 'size',
                  'is_train', 'regit_date', 'register', 'region')

    @staticmethod
    def change_datetime(data) -> dict:
        date_time = data['regit_date'].replace('T', '일 ').replace('-', '년', 1).replace('-', '월') \
            .replace(':', '시', 1).replace(':', '분')
        data['regit_date'] = date_time[:date_time.find('분') + 1]
        return data


class NormalShipUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NormalShip
        fields = '__all__'


class NormalImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NormalImage
        fields = ('id', 'img', 'regit_date')


class WasteShipSerializer(serializers.HyperlinkedModelSerializer):
    register = serializers.SlugRelatedField(read_only=True,
                                            many=False,
                                            slug_field='srvno')

    class Meta:
        model = WasteShip
        fields = ('id', 'main_img', 'info', 'types', 'lat', 'lon',
                  'is_train', 'regit_date', 'register')


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
        fields = ('id', 'lat', 'lon', 'info')


class ProgramNormalShipSerializer(serializers.HyperlinkedModelSerializer):
    normal_imgs = serializers.StringRelatedField(many=True)

    class Meta:
        model = NormalShip
        fields = ('name', 'img_cnt', 'normal_imgs', 'main_img')


class ProgramWasteShipSerializer(serializers.HyperlinkedModelSerializer):
    waste_imgs = serializers.StringRelatedField(many=True)

    class Meta:
        model = WasteShip
        fields = ('id', 'img_cnt', 'waste_imgs', 'main_img')