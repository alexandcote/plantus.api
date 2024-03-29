import uuid

from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    SerializerMethodField,
    UUIDField
)
from rest_framework.serializers import ModelSerializer

from places.models import Place
from pots.models import (
    Pot,
    TimeSerie,
    Operation
)


class PotSerializer(ModelSerializer):
    class Meta:
        model = Pot
        fields = (
            'id',
            'name',
            'picture',
            'identifier',
            'url',
        )


class TimeSeriesSerializer(ModelSerializer):

    pot_identifier = UUIDField(
        source='pot.identifier', write_only=True, required=True)

    pot = PotSerializer(read_only=True)

    class Meta:
        model = TimeSerie
        fields = (
            'id',
            'date',
            'temperature',
            'humidity',
            'luminosity',
            'water_level',
            'pot_identifier',
            'pot'
        )
        extra_kwargs = {'pot': {'read_only': True}}

    def __init__(self, *args, **kwargs):
        super(TimeSeriesSerializer, self).__init__(*args, **kwargs)
        nested = kwargs['context'].get('nested', True)

        if not nested:
            self.fields.pop('pot')

    def get_fields(self):
        fields = super(TimeSeriesSerializer, self).get_fields()
        user = self.context['request'].user

        if user.is_anonymous:
            identifier = self.context['request'].META.get(
                'HTTP_X_AUTHORIZATION', '')

            try:
                identifier = uuid.UUID(identifier)
                self.context['current_place'] = Place.objects.filter(
                    identifier=identifier)

                fields['pot'].queryset = Pot.objects.filter(
                    place=self.context['current_place'])
            except ValueError:
                pass

        elif not user.is_superuser:
            fields['pot'].queryset = Pot.objects.filter(place__users=user.id)

        return fields

    def validate_pot_identifier(self, value):
        place = self.context['current_place']
        if not Pot.objects.filter(place=place, identifier=value).exists():
            raise ValidationError(
                "Invalid identifier '{identifier}' - object does "
                "not exist.".format(identifier=value))
        return value

    def create(self, validated_data):
        pot_identifier = validated_data['pot']['identifier']
        validated_data['pot'] = Pot.objects.get(identifier=pot_identifier)
        return TimeSerie.objects.create(**validated_data)


class PotsSerializer(ModelSerializer):
    spec = SerializerMethodField()

    class Meta:
        model = Pot
        fields = (
            'id',
            'name',
            'picture',
            'identifier',
            'place',
            'plant',
            'spec',
            'url',
        )
        extra_kwargs = {'identifier': {'required': True}}

    def __init__(self, *args, **kwargs):
        super(PotsSerializer, self).__init__(*args, **kwargs)

        # Can't update the identifier of a place.
        view = self.context.get('view', None)
        if view and hasattr(view, 'action') and \
                view.action in ['update', 'partial_update']:
            self.fields['identifier'].read_only = True

    def get_spec(self, obj):
        if hasattr(obj, 'current_spec') and len(obj.current_spec) > 0:
            return TimeSeriesSerializer(obj.current_spec[0], context={
                'request': self.context['request'], 'nested': False}).data
        return None

    def get_fields(self):
        fields = super(PotsSerializer, self).get_fields()
        user = self.context['request'].user

        if not user.is_superuser:
            fields['place'].queryset = Place.objects.filter(users=user.id)

        return fields


class OperationsSerializer(ModelSerializer):
    pot_identifier = UUIDField(source='pot.identifier')

    class Meta:
        model = Operation
        fields = (
            'id',
            'action',
            'pot',
            'url',
            'pot_identifier',
            'created_at',
            'completed_at',
        )

    def __init__(self, *args, **kwargs):
        super(OperationsSerializer, self).__init__(*args, **kwargs)

        user = self.context['request'].user

        if user.is_anonymous:
            self.fields['pot'].read_only = True
        else:
            self.fields['pot_identifier'].read_only = True

    def get_fields(self):
        fields = super(OperationsSerializer, self).get_fields()
        user = self.context['request'].user

        if user.is_anonymous:
            identifier = self.context['request'].META.get(
                'HTTP_X_AUTHORIZATION', '')

            try:
                identifier = uuid.UUID(identifier)
                self.context['current_place'] = Place.objects.filter(
                    identifier=identifier)

                fields['pot'].queryset = Pot.objects.filter(
                    place=self.context['current_place'])
            except ValueError:
                pass

        elif not user.is_superuser:
            fields['pot'].queryset = Pot.objects.filter(place__users=user.id)

        return fields

    def validate(self, data):
        pot = data['pot']
        action = data['action']
        if Operation.objects.filter(
                pot=pot, action=action, completed_at__isnull=True).exists():
            raise ValidationError("Action already exist for this pot")

        return data
