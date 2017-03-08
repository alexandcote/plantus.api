from rest_framework.serializers import ModelSerializer
from places.models import Place
from places.services import create_place, update_place


class PlaceSerializer(ModelSerializer):

    class Meta:
        model = Place
        fields = (
            'id',
            'name',
            'url',
            'users'
        )

    def create(self, validated_data):
        """
        Create a place with the data.
        """

        # Set the current user to a place if no users are passed
        users = validated_data.get('users', None)
        if not users:
            validated_data['users'] = [self.context['request'].user]

        place = create_place(validated_data)
        return place

    def update(self, instance, validated_data):
        """
        Update the place instance with the data.
        """
        place = update_place(instance, validated_data)
        return place
