from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from places.models import Place


class PlaceSerializer(ModelSerializer):
    users_listing = HyperlinkedIdentityField(view_name='place-users')

    class Meta:
        model = Place
        fields = (
            'id',
            'name',
            'ip_address',
            'port',
            'url',
            'users',
            'users_listing'
        )
        extra_kwargs = {
            'users': {'required': False},
        }
