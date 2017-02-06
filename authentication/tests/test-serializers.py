from django.test import TestCase

from authentication.serializers import UserSerializer


class TestUserSerializer(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'Wayne',
            'last_name': 'Gretzky',
            'email': 'wayne.gretzky@plantustest.com',
            'password': 'qwer1234',
        }

    def test_empty_user(self):
        """
        Create a user empty user should have those fields
        """
        serializer = UserSerializer()
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
        }
        self.assertEqual(serializer.data, data)

    def test_required_fields(self):
        """
        Create a empty user should required those fields
        """
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
        """
        Create a user with minimum data
        """
        serializer = UserSerializer(data=self.data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
