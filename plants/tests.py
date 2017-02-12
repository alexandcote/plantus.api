from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from authentication.factories import SuperUserFactory, UserFactory
from plants.factories import PlantFactory
from plants.models import Plant


class TestsPlantCreate(APITestCase):

    def setUp(self):
        self.plant = PlantFactory()
        self.superuser = SuperUserFactory()

    def test_plant_create_normal_user(self):
        """
        Ensure that we couldn't create a plant
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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plant_create_super_user(self):
        """
        Ensure super user can create a plant
        """
        url = reverse('plant-list')
        self.client.force_authenticate(user=self.superuser)

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
        Ensure superuser can't create an empty plant
        """
        url = reverse('plant-list')
        self.client.force_authenticate(user=self.superuser)

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

    def test_plant_list(self):
        """
        Ensure that user can list all plants
        """
        url = reverse('plant-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.plant.id)
        self.assertEqual(result[0]['name'], self.plant.name)
        self.assertEqual(
            Decimal(result[0]['humidity_spec']),
            self.plant.humidity_spec)
        self.assertEqual(
            Decimal(result[0]['luminosity_spec']),
            self.plant.luminosity_spec)
        self.assertEqual(
            Decimal(result[0]['temperature_spec']),
            self.plant.temperature_spec)


class TestsPlantRetrieve(APITestCase):

    def setUp(self):
        self.plant = PlantFactory()

    def test_plant_retrieve(self):
        """
        Ensure that user can retrieve plants by id
        """
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestsPlantUpdate(APITestCase):

    def setUp(self):
        self.plant = PlantFactory()
        self.user = UserFactory()
        self.superuser = SuperUserFactory()

    def test_plant_partial_update(self):
        """
        Ensure that the plant information are not updated for normal user
        """
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        self.client.force_authenticate(user=self.user)

        data = {"name": "Rose", "description": "Une belle rose"}
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plant_partial_update_super(self):
        """
        Ensure that the plant information are correctly updated(SuperUser)
        """
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        self.client.force_authenticate(user=self.superuser)

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plant_full_update_super(self):
        """
        Ensure that the user information are correctly updated with put(
        SuperUser)
        """
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        self.client.force_authenticate(user=self.superuser)

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
        self.user = UserFactory()
        self.superuser = SuperUserFactory()

    def test_plant_delete_normal_users(self):
        """
        Ensure that user can't delete a plant
        """
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plant_delete_super_users(self):
        """
        Ensure that super user can delete a plant
        """
        url = reverse('plant-detail', kwargs={"pk": self.plant.pk})
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestsPlantSearch(APITestCase):
    def setUp(self):
        self.plant = PlantFactory()
        self.plant2 = PlantFactory()

    def test_plant_search_by_name(self):
        """
        Ensure that user can search a plant by the name
        """
        url = reverse('plant-list')
        url += "?search={search}".format(search=self.plant.name)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])
        self.assertEqual(len(result), 1)

        self.assertEqual(result[0]['id'], self.plant.id)
        self.assertEqual(result[0]['name'], self.plant.name)
        self.assertEqual(
            Decimal(result[0]['humidity_spec']),
            self.plant.humidity_spec)
        self.assertEqual(
            Decimal(result[0]['luminosity_spec']),
            self.plant.luminosity_spec)
        self.assertEqual(
            Decimal(result[0]['temperature_spec']),
            self.plant.temperature_spec)

    def test_plant_search_by_desc(self):
        """
        Ensure that user can search a plant by the description
        """
        url = reverse('plant-list')
        url += "?search={search}".format(search=self.plant2.description)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.plant2.id)
        self.assertEqual(result[0]['name'], self.plant2.name)
        self.assertEqual(
            Decimal(result[0]['humidity_spec']),
            self.plant2.humidity_spec)
        self.assertEqual(
            Decimal(result[0]['luminosity_spec']),
            self.plant2.luminosity_spec)
        self.assertEqual(
            Decimal(result[0]['temperature_spec']),
            self.plant2.temperature_spec)

    def test_plant_search_all(self):
        """
        Ensure that user can search all the plants
        """
        url = reverse('plant-list')
        url += "?search={search}".format(search='')
        response = self.client.get(url, format='json')
        result = response.data
        self.assertEqual(result['count'], 2)

    def test_plant_search_fail(self):
        """
        Ensure that user can do a wrong search without any result
        """
        url = reverse('plant-list')
        # do a search with junk
        url += "?search={search}".format(search='alkdjslkjdfl')
        response = self.client.get(url, format='json')
        result = response.data
        self.assertEqual(result['count'], 0)
