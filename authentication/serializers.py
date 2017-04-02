from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.compat import PasswordField

from authentication.models import User
from authentication.services import (
    create_user,
    update_user
)


class UserSerializer(ModelSerializer):
    password = PasswordField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'url',
        )

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
