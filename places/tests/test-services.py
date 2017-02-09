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
        self.assertEqual(place.ip_address, '0.0.0.0')
        self.assertEqual(place.port, 0)
        self.assertEqual(Place.objects.count(), 1)

    def test_create_place(self):
        """
        Create a place with create_place service
        """
        data = {
            'name': 'Ismael',
            'ip_address': '127.15.0.0',
            'port': '9'
        }
        place = create_place(data=data)

        self.assertEqual(place.name, data['name'])
        self.assertEqual(place.ip_address, data['ip_address'])
        self.assertEqual(place.port, data['port'])
        self.assertEqual(Place.objects.count(), 1)

    def test_create_place_with_users(self):
        """
        Create a place with create_place service
        """
        user = UserFactory()
        user2 = UserFactory()
        data = {
            'name': 'Ismael',
            'ip_address': '127.15.0.0',
            'port': '9',
            'users': [user.id, user2.id]
        }
        place = create_place(data=data)

        self.assertEqual(place.name, data['name'])
        self.assertEqual(place.ip_address, data['ip_address'])
        self.assertEqual(place.port, data['port'])
        self.assertEqual(place.users.count(), 2)
        self.assertEqual(Place.objects.count(), 1)


class TestUpdatePlace(TestCase):

    def setUp(self):
        self.place = PlaceFactory()

    def test_update_place(self):
        """
        Update place with update_place service
        """
        data = {
            'name': 'Carl',
            'ip_address': '127.16.0.0',
            'port': '3'
        }
        place = update_place(place=self.place, data=data)
        self.assertEqual(place.name, data['name'])
        self.assertEqual(place.ip_address, data['ip_address'])
        self.assertEqual(place.port, data['port'])
        self.assertEqual(Place.objects.count(), 1)

    def test_update_place_with_users(self):
        """
        Update place with update_place service
        """
        user = UserFactory()
        data = {
            'name': 'Carl',
            'ip_address': '127.16.0.0',
            'port': '3',
            'users': [user.id]
        }

        place = update_place(place=self.place, data=data)
        self.assertEqual(place.name, data['name'])
        self.assertEqual(place.ip_address, data['ip_address'])
        self.assertEqual(place.port, data['port'])
        self.assertEqual(Place.objects.count(), 1)

        for user in place.users.all():
            self.assertTrue(user.id in data['users'])
