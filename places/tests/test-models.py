from django.test import TestCase

from places.factories import PlaceFactory


class TestModel(TestCase):

    def setUp(self):
        self.place = PlaceFactory()

    def test_get__str__(self):
        self.assertEqual(self.place.__str__(), self.place.name)
