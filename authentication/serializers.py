from rest_framework.serializers import ModelSerializer

from authentication.models import User
from authentication.services import (
    create_user,
    update_user
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'url',
            'places'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'places': {'read_only': True},
        }

    def create(self, validated_data):
        """
        Create a user with the data.
        """
        user = create_user(validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Update the user instance with the data.
        """
        user = update_user(instance, validated_data)
        return user
