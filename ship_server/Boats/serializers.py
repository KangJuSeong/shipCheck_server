from rest_framework import serializers
from Boats.models import Boat, WasteBoat, BoatImg


class BoatImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BoatImg
        fields = '__all__'


class BoatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Boat
        fields = '__all__'


class WasteBoatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteBoat
        fields = '__all__'