from django.test import TestCase

from authentication.factories import UserFactory
from places.factories import PlaceFactory
from places.models import Place
from places.services import update_place, create_place


class TestCreatePlace(TestCase):

    def test_create_empty_place(self):
        """
        Create a empty place with create_place service
        """
        place = create_place({})
        self.assertEqual(place.name, '')
        self.assertEqual(Place.objects.count(), 1)

    def test_create_place(self):
        """
        Create a place with create_place service
        """
        data = {'name': 'Ismael'}
        place = create_place(data=data)

        self.assertEqual(place.name, data['name'])
        self.assertEqual(Place.objects.count(), 1)

    def test_create_place_with_users(self):
        """
        Create a place with create_place service
        """
        user = UserFactory()
        user2 = UserFactory()
        data = {
            'name': 'Ismael',
            'users': [user.id, user2.id]
        }
        place = create_place(data=data)

        self.assertEqual(place.name, data['name'])
        self.assertEqual(place.users.count(), 2)
        self.assertEqual(Place.objects.count(), 1)


class TestUpdatePlace(TestCase):

    def setUp(self):
        self.place = PlaceFactory()

    def test_update_place(self):
        """
        Update place with update_place service
        """
        data = {'name': 'Carl'}
        place = update_place(place=self.place, data=data)
        self.assertEqual(place.name, data['name'])
        self.assertEqual(Place.objects.count(), 1)

    def test_update_place_with_users(self):
        """
        Update place with update_place service
        """
        user = UserFactory()
        data = {
            'name': 'Carl',
            'users': [user.id]
        }

        place = update_place(place=self.place, data=data)
        self.assertEqual(place.name, data['name'])
        self.assertEqual(Place.objects.count(), 1)

        for user in place.users.all():
            self.assertTrue(user.id in data['users'])
