from rest_framework.serializers import ModelSerializer

from places.models import Place
from pots.models import Pot


class PotSerializer(ModelSerializer):

    class Meta:
        model = Pot
        fields = (
            'id',
            'name',
            'place',
            'plant',
            'url',
        )

    def get_fields(self):
        fields = super(PotSerializer, self).get_fields()
        user = self.context['request'].user

        if not user.is_superuser:
            fields['place'].queryset = Place.objects.filter(users=user.id)

        return fields
