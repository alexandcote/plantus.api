from rest_framework.serializers import ModelSerializer

from places.models import Place
from pots.models import Pot, TimeSerie


class TimeSeriesSerializer(ModelSerializer):

    class Meta:
        model = TimeSerie
        fields = (
            'id',
            'date',
            'temperature',
            'humidity',
            'luminosity',
            'water_level',
            'url'
        )


class PotSerializer(ModelSerializer):
    time_series = TimeSeriesSerializer(source="last_timeseries",
                                       read_only=True)

    class Meta:
        model = Pot
        fields = (
            'id',
            'name',
            'place',
            'plant',
            'time_series',
            'url',
        )

    def get_fields(self):
        fields = super(PotSerializer, self).get_fields()
        user = self.context['request'].user

        if not user.is_superuser:
            fields['place'].queryset = Place.objects.filter(users=user.id)

        return fields
