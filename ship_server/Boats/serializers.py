from rest_framework import serializers
from Boats.models import Boat, WasteBoat


class BoatSerializer(serializers.HyperlinkedModelSerializer):
    boat_img = serializers.ImageField(use_url=True)

    class Meta:
        model = Boat
        fields = ('id', 'title', 'price', 'reserve', 'product_status',
                  'manufacturer', 'brand', 'model_code', 'boat_img')


class BoatSearchingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Boat
        fields = ('id', 'title', 'price', 'manufacturer')


class BoatDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Boat
        fields = ('title', 'price', 'reserve', 'product_status',
                  'manufacturer', 'brand', 'model_code', 'boat_img')


class WasteBoatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WasteBoat
        fields = ('id', 'title', 'latitude', 'longitude')