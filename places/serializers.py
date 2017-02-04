from rest_framework.serializers import ModelSerializer, \
    HyperlinkedModelSerializer

from places.models import Place


class PlaceSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = (
            'id',
            'name',
            'ip_address',
            'port',
            'url',
            'users'
        )


class SimplePlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = (
            'id',
            'name',
            'ip_address',
            'port',
            'url'
        )
