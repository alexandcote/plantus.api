from django.test import TestCase

from authentication.factories import UserFactory
from authentication.models import User
from authentication.services import create_user, update_user


class TestCreateUser(TestCase):
    def test_create_normal_user(self):
        """
        Create a normal user with the create_user service
        """
        data = {
            'first_name': 'Wayne',
            'last_name': 'Gretzky',
            'email': 'wayne.gretzky@plantustest.com',
            'password': 'qwer1234'
        }
        user = create_user(data=data)

        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(User.objects.count(), 1)

    def test_create_super_user(self):
        """
        Create a superuser with the create_user service
        """
        data = {
            'first_name': 'Wayne',
            'last_name': 'Gretzky',
            'email': 'wayne.gretzky@plantustest.com',
            'password': 'qwer1234',
            'is_staff': True,
            'is_superuser': True
        }
        user = create_user(data=data)

        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(User.objects.count(), 1)


class TestUpdateUser(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_create_normal_user(self):
        """
        Update a user with the update_user service
        """
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new.user@plantustest.com',
            'password': 'new_user',
            'is_staff': True,
            'is_superuser': True
        }
        user = update_user(user=self.user, data=data)
        new_user = User.objects.get(id=self.user.id)

        self.assertEqual(user.id, new_user.id)
        self.assertEqual(new_user.first_name, data["first_name"])
        self.assertEqual(new_user.last_name, data["last_name"])
        self.assertEqual(new_user.email, data["email"])
        self.assertTrue(new_user.check_password(data["password"]))
        self.assertTrue(new_user.is_staff)
        self.assertTrue(new_user.is_superuser)
