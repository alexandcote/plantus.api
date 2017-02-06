from django.test import TestCase
from django.utils import timezone

from authentication.models import (
    User,
    UserManager
)


class TestUser(TestCase):
    def setUp(self):
        self.user = User(first_name='Wayne', last_name='Gretzky',
                         email='wayne.gretzky@plantustest.com', is_staff=False,
                         created_at=timezone.now(), updated_at=timezone.now())

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'Wayne')

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'Wayne Gretzky')


class TestUserManager(TestCase):
    def setUp(self):
        self.manager = UserManager()
        self.manager.model = User

    def test_create_basic_user(self):
        user = self.manager.create_user(email='wayne.gretzky@plantustest.com',
                                        password='qwer1234')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().id, user.id)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_create_superuser(self):
        user = self.manager.create_superuser(
            email='wayne.gretzky@plantustest.com', password='qwer1234')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().id, user.id)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

    def test_create_invalid_superuser(self):
        with self.assertRaises(ValueError):
            self.manager.create_superuser(
                email='wayne.gretzky@plantustest.com', password='qwer1234',
                is_staff=False)

        with self.assertRaises(ValueError):
            self.manager.create_superuser(
                email='wayne.gretzky@plantustest.com', password='qwer1234',
                is_superuser=False)
