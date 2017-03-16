import uuid

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from places.models import Place
from pots.models import (
    Pot,
    TimeSerie
)


class TimeSeriesSerializer(ModelSerializer):

    class Meta:
        model = TimeSerie
        fields = (
            'date',
            'temperature',
            'humidity',
            'luminosity',
            'water_level',
            'pot'
        )

        extra_kwargs = {'pot': {'write_only': True}}

    def get_fields(self):
        fields = super(TimeSeriesSerializer, self).get_fields()
        user = self.context['request'].user

        if user.is_anonymous:
            identifier = self.context['request'].META.get(
                'HTTP_X_AUTHORIZATION', '')

            try:
                identifier = uuid.UUID(identifier)
                fields['pot'].queryset = Pot.objects.filter(
                    place__identifier=identifier)
            except ValueError:
                pass

        elif not user.is_superuser:
            fields['pot'].queryset = Pot.objects.filter(place__users=user.id)

        return fields


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
            return TimeSeriesSerializer(obj.current_spec[0], context={
                'request': self.context['request']}).data
        return None

    def get_fields(self):
        fields = super(PotSerializer, self).get_fields()
        user = self.context['request'].user

        if not user.is_superuser:
            fields['place'].queryset = Place.objects.filter(users=user.id)

        return fields
