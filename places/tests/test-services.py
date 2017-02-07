from django.test import TestCase

from places.factories import PlaceFactory
from places.models import Place
from places.services import update_place, create_place

# TODO: Aouter les tests pour les users dans la creation et l'update des places
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
        self.assertEqual(place.port, data['port'])
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

    def test_update_empty_place(self):
        """
        Update a place with no parameters with update_place service
        """
        place = update_place(place=self.place, data={})
        self.assertEqual(place.name, self.place.name)
        self.assertEqual(place.ip_address, self.place.ip_address)
        self.assertEqual(place.port, self.place.port)
        self.assertEqual(Place.objects.count(), 1)
