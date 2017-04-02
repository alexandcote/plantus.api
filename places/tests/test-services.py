import uuid

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
        place = Place.objects.get(id=place.id)

        self.assertEqual(place.name, '')
        self.assertEqual(Place.objects.count(), 1)

    def test_create_place(self):
        """
        Create a place with create_place service
        """
        data = {'name': 'Ismael'}
        place = create_place(data=data)
        place = Place.objects.get(id=place.id)

        self.assertEqual(place.name, data['name'])
        self.assertEqual(Place.objects.count(), 1)

    def test_create_place_with_identifier(self):
        """
        Create a place with create_place service
        """
        data = {
            'name': 'Ismael',
            'identifier': uuid.uuid4()
        }
        place = create_place(data=data)
        place = Place.objects.get(id=place.id)

        self.assertEqual(place.name, data['name'])
        self.assertEqual(place.identifier, data['identifier'])
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
        place = Place.objects.get(id=place.id)

        self.assertEqual(place.name, data['name'])
        self.assertEqual(place.users.count(), 2)
        self.assertEqual(Place.objects.count(), 1)


class TestUpdatePlace(TestCase):

    def setUp(self):
        self.place = PlaceFactory()

    def test_update_place(self):
        """
        Update place with update_place service should change name
        """
        data = {'name': 'Carl'}
        place = update_place(place=self.place, data=data)
        place = Place.objects.get(id=place.id)

        self.assertEqual(place.name, data['name'])
        self.assertEqual(Place.objects.count(), 1)

    def test_update_place_with_identifier(self):
        """
        Update place with update_place service should not change the identifier
        """
        data = {
            'name': 'Carl',
            'identifier': uuid.uuid4()
        }
        place = update_place(place=self.place, data=data)
        place = Place.objects.get(id=place.id)

        self.assertEqual(place.name, data['name'])
        self.assertNotEqual(place.identifier, data['identifier'])
        self.assertEqual(place.identifier, self.place.identifier)
        self.assertEqual(Place.objects.count(), 1)

    def test_update_place_with_users(self):
        """
        Update place with update_place service should add users and change name
        """
        user = UserFactory()
        data = {
            'name': 'Carl',
            'users': [user.id]
        }

        place = update_place(place=self.place, data=data)
        place = Place.objects.get(id=place.id)

        self.assertEqual(place.name, data['name'])
        self.assertEqual(Place.objects.count(), 1)

        for user in place.users.all():
            self.assertTrue(user.id in data['users'])
