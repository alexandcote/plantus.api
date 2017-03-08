from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authentication.factories import UserFactory
from places.factories import PlaceFactory
from plants.factories import PlantFactory
from pots.factories import PotFactory
from pots.models import Pot


class TestsPotCreate(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.place = PlaceFactory(users=[self.user.id])
        self.place2 = PlaceFactory()
        self.plant = PlantFactory()

    def test_create_pot(self):
        """
        Ensure that we could create a pot
        """
        url = reverse('pot-list')
        data = {
            'name': 'Pot #1',
            'place': self.place.id,
            'plant': self.plant.id,
        }
        self.client.force_authenticate(user=self.user)
        self.assertEqual(Pot.objects.count(), 0)

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = response.data
        self.assertEquals(result['name'], data['name'])
        self.assertEquals(result['place'], data['place'])
        self.assertEquals(result['plant'], data['plant'])
        self.assertEqual(Pot.objects.count(), 1)

    def test_create_on_other_user_place(self):
        """
        Ensure that we could create a pot
        """
        url = reverse('pot-list')
        data = {
            'name': 'Pot #1',
            'place': self.place2.id,
            'plant': self.plant.id,
        }
        self.client.force_authenticate(user=self.user)
        self.assertEqual(Pot.objects.count(), 0)

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Pot.objects.count(), 0)

    def test_create_empty_pot(self):
        """
        Ensure that we need parameters to create a pot
        """
        url = reverse('pot-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)

        expected_error = {
            'name': ['This field is required.'],
            'place': ['This field is required.'],
            'plant': ['This field is required.']
        }
        self.assertEqual(response.data, expected_error)


class TestPotsList(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.place2 = PlaceFactory(users=(self.user2,))
        self.pot1 = PotFactory(place=self.place)
        self.pot2 = PotFactory(place=self.place)
        self.pot3 = PotFactory(place=self.place2)

    def test_place_list(self):
        """
        Ensure that a user can list only his pots
        """
        url = reverse('pot-list')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], self.pot1.id)
        self.assertEqual(result[1]['id'], self.pot2.id)

    def test_place_list_unauthenticated(self):
        """
        Ensure that not log users can't list pots
        """
        url = reverse('pot-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUpdatePots(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.place2 = PlaceFactory(users=(self.user2,))
        self.plant = PlantFactory()
        self.pot = PotFactory(place=self.place)
        self.pot2 = PotFactory(place=self.place2)

    def test_update_pot(self):
        """
       Ensure that we could update a pot
       """
        url = reverse('pot-detail', kwargs={"pk": self.pot.pk})
        data = {
            'name': 'Pot #1',
            'place': self.place.id,
            'plant': self.plant.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pot = Pot.objects.get(id=self.pot.id)
        self.assertEquals(pot.name, data['name'])
        self.assertEquals(pot.place.id, data['place'])
        self.assertEquals(pot.plant.id, data['plant'])

        # Without plant should raise a Bad Request
        data.pop('plant')
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_pot(self):
        """
        Ensure that a patch works
        """
        url = reverse('pot-detail', kwargs={"pk": self.pot.pk})
        data = {
            'name': 'Pot #2',
            'plant': self.plant.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pot = Pot.objects.get(id=self.pot.id)
        self.assertEquals(pot.name, data['name'])
        self.assertEquals(pot.place.id, self.place.id)
        self.assertEquals(pot.plant.id, self.plant.id)

        data = {'place': self.place2.id}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_other_user_pot(self):
        """
        Ensure that you cannot update someone else pot
        """
        url = reverse('pot-detail', kwargs={"pk": self.pot2.pk})
        data = {'name': 'Error #1'}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeletePots(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.pot = PotFactory(place=self.place)

    def test_delete_pot(self):
        """
        Ensure that a Delete should returns No Content
        """
        url = reverse('pot-detail', kwargs={"pk": self.pot.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_pot(self):
        """
        Ensure you cannot delete other user pot
        """
        url = reverse('pot-detail', kwargs={"pk": self.pot.pk})
        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestRetrievePot(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.plant = PlantFactory()
        self.pot = PotFactory(place=self.place, plant=self.plant)

    def test_retrieve_pot(self):
        """
        Ensure you can retrieve a pot
        """
        url = reverse('pot-detail', kwargs={"pk": self.pot.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = response.data
        self.assertEquals(result['name'], self.pot.name)
        self.assertEquals(result['place'], self.place.id)
        self.assertEquals(result['plant'], self.plant.id)

    def test_retrieve_other_place(self):
        """
        Ensure you cannot retrieve other user pot
        """
        url = reverse('pot-detail', kwargs={"pk": self.pot.pk})
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSearchPot(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.place2 = PlaceFactory(users=(self.user2,))
        self.pot = PotFactory(place=self.place)
        self.pot2 = PotFactory(place=self.place2)

    def test_pot_filter_by_user(self):
        """
        Ensure you can filter a pot by user
        """
        url = reverse('pot-list')
        url += "?place__users={search}".format(search=self.user.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.pot.id)

    def test_pot_filter_by_other_user(self):
        """
        Ensure you can't filter a pot from an other user
        """
        url = reverse('pot-list')
        url += "?place__users={search}".format(search=self.user2.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])

        self.assertEqual(len(result), 0)

    def test_pot_filter_by_place(self):
        """
        Ensure you can filter a pot by place
        """
        url = reverse('pot-list')
        url += "?place={search}".format(search=self.place.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.pot.id)

    def test_pot_filter_by_other_user_place(self):
        """
        Ensure you can't filter a pot from an other user place
        """
        url = reverse('pot-list')
        url += "?place={search}".format(search=self.place2.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])

        self.assertEqual(len(result), 0)


class TestsPotAction(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=[self.user.id])
        self.plant = PlantFactory()
        self.pot = PotFactory(place=self.place, plant=self.plant)

    def test_water_a_other_user_pot(self):
        url = reverse('pot-water', kwargs={"pk": self.pot.pk})
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch('pots.views.service_to_water_pot')
    def test_water_a_pot(self, mock_service_to_water_pot):
        url = reverse('pot-water', kwargs={"pk": self.pot.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        mock_service_to_water_pot.assert_called_once_with(self.pot)
