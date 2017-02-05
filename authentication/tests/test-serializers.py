from django.test import TestCase

from authentication.serializers import UserSerializer
from places.factories import PlaceFactory


class TestUserSerializer(TestCase):
    def setUp(self):
        self.place = PlaceFactory()
        self.data = {
            'first_name': 'Wayne',
            'last_name': 'Gretzky',
            'email': 'wayne.gretzky@plantustest.com',
            'password': 'qwer1234',
        }

    def test_empty_user(self):
        serializer = UserSerializer()
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
        }
        self.assertEqual(serializer.data, data)

    def test_required_fields(self):
        serializer = UserSerializer(data={})
        is_valid = serializer.is_valid()

        expected_error = {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'email': ['This field is required.'],
            'password': ['This field is required.']
        }

        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, expected_error)

    def test_create(self):
        serializer = UserSerializer(data=self.data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
