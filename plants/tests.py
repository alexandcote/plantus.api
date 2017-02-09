from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from authentication.factories import SuperUserFactory
from plants.factories import PlantFactory
from plants.models import Plant


class TestsPlantCreate(APITestCase):

    def setUp(self):
        self.plant = PlantFactory()

    def test_plant_create(self):
        """
        Ensure that we could create a plant
        """
        url = reverse('plant-list')
        data = {
            'name': 'Rose',
            'description': 'Description de la rose',
            'humidity_spec': '45.2',
            'luminosity_spec': '12.32',
            'temperature_spec': '1.3'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        plant = Plant.objects.get(name='Rose')
        self.assertEquals(plant.name, data['name'])
        self.assertEquals(plant.description, data['description'])
        self.assertEquals(plant.humidity_spec, Decimal(data['humidity_spec']))
        self.assertEquals(
            plant.luminosity_spec, Decimal(data['luminosity_spec']))
        self.assertEquals(
            plant.temperature_spec, Decimal(data['temperature_spec']))

    def test_empty_plant(self):
        """
        Ensure that we cant't create an empty plant
        """
        url = reverse('plant-list')
        data = {
            'name': '',
            'description': '',
            'humidity_spec': '',
            'luminosity_spec': '',
            'temperature_spec': ''
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestsPlantList(APITestCase):

    def setUp(self):
        self.plant = PlantFactory()

    def test_users_list(self):
        """
        Ensure that user can list all plants
        """
        url = reverse('plant-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestsPlantRetrieve(APITestCase):

    def setUp(self):
        self.plant = PlantFactory()

    def test_plant_retrieve(self):
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestsPlantUpdate(APITestCase):

    def setUp(self):
        self.plant = PlantFactory()
        self.user = SuperUserFactory()

    def test_plant_partial_update(self):
        """
         Ensure that the plant information are correctly updated
         """
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        self.client.force_authenticate(user=self.user)

        data = {"name": "Rose", "description": "Une belle rose"}
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        plant = Plant.objects.get(pk=self.plant.pk)
        self.assertEqual(plant.name, data["name"])
        self.assertEqual(plant.description, data["description"])
        self.assertEqual(plant.temperature_spec, self.plant.temperature_spec)

    def test_plant_full_update(self):
        """
        Ensure that the user information are correctly updated with put
        """
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'Lila',
            'description': 'Description de la lila',
            'humidity_spec': '30.2',
            'luminosity_spec': '52.25',
            'temperature_spec': '10.3'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        plant = Plant.objects.get(pk=self.plant.pk)
        self.assertEqual(plant.name, data['name'])
        self.assertEquals(plant.description, data['description'])
        self.assertEquals(plant.humidity_spec, Decimal(data['humidity_spec']))
        self.assertEquals(
            plant.luminosity_spec, Decimal(data['luminosity_spec']))
        self.assertEquals(
            plant.temperature_spec, Decimal(data['temperature_spec']))


class TestPlantsDelete(APITestCase):

    def setUp(self):
        self.plant = PlantFactory()

    def test_current_users_delete(self):
        """
        Ensure that user can't delete a plant
        """
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
