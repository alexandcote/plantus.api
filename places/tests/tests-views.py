from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authentication.factories import UserFactory
from places.factories import PlaceFactory
from places.models import Place


class TestsPlaceCreate(APITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_place_create(self):
        """
        Ensure that we could create a place
        """
        url = reverse('place-list')
        data = {
            'name': 'Villa #8',
            'ip_address': '192.168.1.7',
            'port': 192,
            'users': [self.user.id],
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        place = Place.objects.get(name='Villa #8')
        self.assertEquals(place.name, data['name'])
        self.assertEquals(place.ip_address, data['ip_address'])
        self.assertEquals(place.port, data['port'])


class TestPlacesList(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place1 = PlaceFactory(users=(self.user,))
        self.place2 = PlaceFactory(users=(self.user2,))
        self.place3 = PlaceFactory(users=())

    def test_place_list(self):
        """
        Ensure that normal user can list his places
        """
        url = reverse('place-list')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.place1.id)
        self.assertEqual(result[0]['name'], self.place1.name)
        self.assertEqual(result[0]['ip_address'], self.place1.ip_address)
        self.assertEqual(result[0]['port'], self.place1.port)

    def test_place_list_unavaible(self):
        """
        Ensure that normal user can't list all places
        """
        url = reverse('place-list')
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data
        self.assertEqual(len(result), 1)
        self.assertNotEqual(result[0]['name'], self.place1.name)
        self.assertEqual(result[0]['name'], self.place2.name)
        self.assertNotEqual(result[0]['name'], self.place3.name)
