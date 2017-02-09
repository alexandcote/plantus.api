from rest_framework.serializers import ModelSerializer

from plants.models import Plant


class PlantSerializer(ModelSerializer):

    class Meta:
        model = Plant
        fields = (
            'id',
            'name',
            'description',
            'humidity_spec',
            'luminosity_spec',
            'temperature_spec',
            'url',
        )
