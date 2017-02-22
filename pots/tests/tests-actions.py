from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authentication.factories import UserFactory
from places.factories import PlaceFactory
from plants.factories import PlantFactory
from pots.factories import PotFactory


class TestsPotWater(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.place = PlaceFactory(users=[self.user.id])
        self.plant = PlantFactory()
        self.pot = PotFactory(place=self.place, plant=self.plant)

    @mock.patch('pots.views.service_to_water_pot')
    def test_water_a_pot(self, mock_service_to_water_pot):
        url = reverse('pot-water', kwargs={"pk": self.pot.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        mock_service_to_water_pot.assert_called_once_with(self.pot)

