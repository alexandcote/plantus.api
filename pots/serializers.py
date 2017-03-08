from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from places.models import Place
from pots.models import Pot, TimeSerie


class TimeSeriesSerializer(ModelSerializer):

    class Meta:
        model = TimeSerie
        fields = (
            'date',
            'temperature',
            'humidity',
            'luminosity',
            'water_level'
        )


class PotSerializer(ModelSerializer):
    spec = SerializerMethodField()

    class Meta:
        model = Pot
        fields = (
            'id',
            'name',
            'place',
            'plant',
            'spec',
            'url',
        )

    def get_spec(self, obj):
        if hasattr(obj, 'current_spec') and len(obj.current_spec) > 0:
            return TimeSeriesSerializer(obj.current_spec[0]).data
        return None

    def get_fields(self):
        fields = super(PotSerializer, self).get_fields()
        user = self.context['request'].user

        if not user.is_superuser:
            fields['place'].queryset = Place.objects.filter(users=user.id)

        return fields
