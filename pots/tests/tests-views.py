import uuid
from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authentication.factories import (
    UserFactory,
    SuperUserFactory
)
from places.factories import PlaceFactory
from plants.factories import PlantFactory
from pots.factories import (
    PotFactory,
    TimeSerieFactory,
    OperationFactory,
    OperationCompletedFactory
)
from pots.models import (
    Pot,
    TimeSerie,
    Operation)


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
            'identifier': str(uuid.uuid4()),
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
        self.assertEquals(result['identifier'], data['identifier'])
        self.assertEqual(Pot.objects.count(), 1)

    def test_create_on_other_user_place(self):
        """
        Ensure that we couldn't create a pot on a other user place
        """
        url = reverse('pot-list')
        data = {
            'name': 'Pot #1',
            'identifier': str(uuid.uuid4()),
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
            'identifier': ['This field is required.'],
            'place': ['This field is required.'],
            'plant': ['This field is required.']
        }
        self.assertEqual(response.data, expected_error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
            'identifier': str(uuid.uuid4()),
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pot = Pot.objects.get(id=self.pot.id)
        self.assertEquals(pot.name, data['name'])
        self.assertNotEquals(str(pot.identifier), data['identifier'])
        self.assertEquals(pot.identifier, self.pot.identifier)
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
            'identifier': str(uuid.uuid4())
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pot = Pot.objects.get(id=self.pot.id)
        self.assertEquals(pot.name, data['name'])
        self.assertNotEquals(str(pot.identifier), data['identifier'])
        self.assertEquals(pot.identifier, self.pot.identifier)
        self.assertEquals(pot.place.id, self.place.id)
        self.assertEquals(pot.plant.id, self.plant.id)

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


class TestsTimeSeriesCreate(APITestCase):
    def setUp(self):
        self.user = SuperUserFactory()
        self.place = PlaceFactory(users=[self.user.id])
        self.place2 = PlaceFactory()
        self.pot = PotFactory(place=self.place)
        self.pot2 = PotFactory(place=self.place2)

    def test_create_timeserie_anonymous(self):
        """
        Ensure that we could create a timeseries with an anonymous user
        """
        url = reverse('timeserie-list')
        data = {
            'pot_identifier': str(self.pot.identifier),
            'temperature': Decimal('10'),
            'humidity': Decimal('11'),
            'luminosity': Decimal('12'),
            'water_level': Decimal('13')
        }

        response = self.client.post(
            url, data=data, HTTP_X_AUTHORIZATION=str(self.place.identifier))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.data
        self.assertEquals(Decimal(result['temperature']), data['temperature'])
        self.assertEquals(Decimal(result['humidity']), data['humidity'])
        self.assertEquals(Decimal(result['luminosity']), data['luminosity'])
        self.assertEquals(Decimal(result['water_level']), data['water_level'])
        self.assertEquals(Decimal(result['pot']), self.pot.id)
        self.assertEqual(TimeSerie.objects.count(), 1)

    def test_create_timeserie_bad_identifier(self):
        """
        Ensure that we couldn't create a timeseries with a bad identifier
        """
        url = reverse('timeserie-list')
        data = {
            'pot': self.pot.id,
            'temperature': Decimal('10'),
            'humidity': Decimal('11'),
            'luminosity': Decimal('12'),
            'water_level': Decimal('13')
        }

        response = self.client.post(
            url, data=data, HTTP_X_AUTHORIZATION='potato')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_timeserie_without_pot_identifier(self):
        """
        Ensure that we couldn't create a timeseries without a pot id
        """
        url = reverse('timeserie-list')
        data = {
            'temperature': Decimal('10'),
            'humidity': Decimal('11'),
            'luminosity': Decimal('12'),
            'water_level': Decimal('13')
        }

        response = self.client.post(
            url, data=data, HTTP_X_AUTHORIZATION=str(self.place.identifier))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_timeserie_without_invalid_pot_identifier(self):
        """
        Ensure that we couldn't create a timeseries without a pot id
        """
        url = reverse('timeserie-list')
        data = {
            'pot_identifier': 'potato',
            'temperature': Decimal('10'),
            'humidity': Decimal('11'),
            'luminosity': Decimal('12'),
            'water_level': Decimal('13')
        }

        response = self.client.post(
            url, data=data, HTTP_X_AUTHORIZATION=str(self.place.identifier))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_timeserie_without_other_pot_identifier(self):
        """
        Ensure that we couldn't create a timeseries without a pot id
        """
        url = reverse('timeserie-list')
        data = {
            'pot_identifier': str(self.pot2.identifier),
            'temperature': Decimal('10'),
            'humidity': Decimal('11'),
            'luminosity': Decimal('12'),
            'water_level': Decimal('13')
        }

        response = self.client.post(
            url, data=data, HTTP_X_AUTHORIZATION=str(self.place.identifier))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_timeserie_anonymous_without_identifier(self):
        """
        Ensure that we could create a timeseries without an identifier
        """
        url = reverse('timeserie-list')
        data = {
            'pot': self.pot.id,
            'temperature': Decimal('10'),
            'humidity': Decimal('11'),
            'luminosity': Decimal('12'),
            'water_level': Decimal('13')
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestsTimeSeriesList(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.place = PlaceFactory(users=[self.user])
        self.pot = PotFactory(place=self.place)
        self.timeserie1 = TimeSerieFactory(pot=self.pot)
        self.timeserie2 = TimeSerieFactory(pot=self.pot)
        self.timeserie3 = TimeSerieFactory()

    def test_timeserie_list(self):
        """
        Ensure that a user can list timeseries
        """
        url = reverse('timeserie-list')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], self.timeserie2.id)
        self.assertEqual(result[1]['id'], self.timeserie1.id)

    def test_timeserie_ordering(self):
        """
        Ensure that a user can list timeseries and order it
        """
        self.client.force_authenticate(user=self.user)

        url = "{0}?ordering=date".format(reverse('timeserie-list'))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], self.timeserie1.id)
        self.assertEqual(result[1]['id'], self.timeserie2.id)

        url = "{0}?ordering=-date".format(reverse('timeserie-list'))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], self.timeserie2.id)
        self.assertEqual(result[1]['id'], self.timeserie1.id)

    def test_timeserie_list_unauthenticated(self):
        """
        Ensure that unauthenticated users can't list timeseries
        """
        url = reverse('timeserie-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestRetrieveTimeSeries(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.pot = PotFactory(place=self.place)
        self.timeserie = TimeSerieFactory(pot=self.pot)

    def test_retrieve_timeserie(self):
        """
        Ensure you can retrieve a timeserie
        """
        url = reverse('timeserie-detail', kwargs={"pk": self.timeserie.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = response.data
        self.assertEquals(
            Decimal(result['temperature']), self.timeserie.temperature)
        self.assertEquals(
            Decimal(result['humidity']), self.timeserie.humidity)
        self.assertEquals(
            Decimal(result['luminosity']), self.timeserie.luminosity)
        self.assertEquals(
            Decimal(result['water_level']), self.timeserie.water_level)
        self.assertEquals(result['pot'], self.pot.id)

    def test_retrieve_other_timeserie(self):
        """
        Ensure you cannot retrieve other user timeserie
        """
        url = reverse('timeserie-detail', kwargs={"pk": self.timeserie.pk})
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSearchTimeseries(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.place2 = PlaceFactory(users=(self.user2,))
        self.pot = PotFactory(place=self.place)
        self.pot2 = PotFactory(place=self.place2)
        self.timeserie = TimeSerieFactory(pot=self.pot)
        self.timeserie2 = TimeSerieFactory(pot=self.pot2)

    def test_timeserie_filter_by_place(self):
        """
        Ensure you can filter a timeserie by place
        """
        url = reverse('timeserie-list')
        url += "?pot__place={search}".format(search=self.place.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.timeserie.id)

    def test_timeserie_filter_by_other_user_place(self):
        """
        Ensure you can't filter a timeserie from an other user place
        """
        url = reverse('timeserie-list')
        url += "?pot__place={search}".format(search=self.place2.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])
        self.assertEqual(len(result), 0)

    def test_timeserie_filter_by_pot(self):
        """
        Ensure you can filter a timeserie by pot
        """
        url = reverse('timeserie-list')
        url += "?pot={search}".format(search=self.pot.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.timeserie.id)

    def test_timeserie_filter_by_other_user_pot(self):
        """
        Ensure you can't filter a timeserie from an other user pot
        """
        url = reverse('timeserie-list')
        url += "?pot={search}".format(search=self.pot2.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])
        self.assertEqual(len(result), 0)


class TestOperationsCreate(APITestCase):
    fixtures = ['actions']

    def setUp(self):
        self.user = UserFactory()
        self.place = PlaceFactory(users=[self.user])
        self.place2 = PlaceFactory()
        self.pot = PotFactory(place=self.place)
        self.pot2 = PotFactory(place=self.place2)

    def test_create_operation(self):
        """
        Ensure that we could create a operation with an anonymous user
        """
        url = reverse('operation-list')
        data = {
            'action': 'water',
            'pot': self.pot.id
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.data
        self.assertEquals(result['action'], data['action'])
        self.assertEquals(result['pot'], self.pot.id)
        self.assertEquals(result['completed_at'], None)
        self.assertEqual(Operation.objects.count(), 1)

    def test_create_operation_other_user_pot(self):
        """
        Ensure that we couldn't create a operation on a other user pot
        """
        url = reverse('operation-list')
        data = {
            'action': 'water',
            'pot': self.pot2.id
        }
        self.assertEqual(Operation.objects.count(), 0)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Operation.objects.count(), 0)

    def test_create_empty_operation(self):
        """
        Ensure that we need parameters to create a operation
        """
        url = reverse('operation-list')
        data = {}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data)

        expected_error = {
            'action': ['This field is required.'],
            'pot': ['This field is required.']
        }
        self.assertEqual(response.data, expected_error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestOperationsList(APITestCase):
    fixtures = ['actions']

    def setUp(self):
        self.user = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.place2 = PlaceFactory()
        self.pot1 = PotFactory(place=self.place)
        self.pot2 = PotFactory(place=self.place2)

        self.operation1_1 = OperationCompletedFactory(pot=self.pot1)
        self.operation1_2 = OperationFactory(pot=self.pot1)

        self.operation2_1 = OperationCompletedFactory(pot=self.pot2)
        self.operation2_2 = OperationFactory(pot=self.pot2)

    def test_operation_list(self):
        """
        Ensure that a user can list only his operations
        """
        url = reverse('operation-list')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], self.operation1_2.id)
        self.assertEqual(result[1]['id'], self.operation1_1.id)

    def test_operation_list_unauthenticated(self):
        """
        Ensure that not log users can't list pots
        """
        url = reverse('operation-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_operation_list_x_authorization(self):
        """
        Ensure that a station can list only his operations
        """
        url = reverse('operation-list')

        response = self.client.get(
            url, HTTP_X_AUTHORIZATION=str(self.place.identifier))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], self.operation1_2.id)
        self.assertEqual(result[1]['id'], self.operation1_1.id)


class TestRetrieveOperations(APITestCase):
    fixtures = ['actions']

    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.pot = PotFactory(place=self.place)
        self.operation = OperationFactory(pot=self.pot)
        self.operation2 = OperationFactory()

    def test_retrieve_operation(self):
        """
        Ensure you can retrieve a operation
        """
        url = reverse('operation-detail', kwargs={"pk": self.operation.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = response.data
        self.assertEquals(result['action'], 'water')
        self.assertEquals(result['pot'], self.pot.id)
        self.assertEquals(result['pot_identifier'], str(self.pot.identifier))

    def test_retrieve_other_operation(self):
        """
        Ensure you cannot retrieve other user operation
        """
        url = reverse('operation-detail', kwargs={"pk": self.operation.pk})
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_operation_x_authorization(self):
        """
        Ensure a station can retrieve a operation
        """
        url = reverse('operation-detail', kwargs={"pk": self.operation.pk})

        response = self.client.get(
            url, HTTP_X_AUTHORIZATION=str(self.place.identifier))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = response.data
        self.assertEquals(result['action'], 'water')
        self.assertEquals(result['pot'], self.pot.id)
        self.assertEquals(result['pot_identifier'], str(self.pot.identifier))

    def test_retrieve_operation_other_x_authorization(self):
        """
        Ensure a station can't retrieve a operation of an other station
        """
        url = reverse('operation-detail', kwargs={"pk": self.operation2.pk})

        response = self.client.get(
            url, HTTP_X_AUTHORIZATION=str(self.place.identifier))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestCompletedOperations(APITestCase):
    fixtures = ['actions']

    def setUp(self):
        self.user = UserFactory()
        self.superuser = SuperUserFactory()
        self.place = PlaceFactory(users=[self.user])
        self.place2 = PlaceFactory()
        self.pot = PotFactory(place=self.place)
        self.pot2 = PotFactory(place=self.place2)
        self.operation = OperationFactory(pot=self.pot)
        self.operation2 = OperationFactory(pot=self.pot2)

    def test_completed_operation_x_authorization(self):
        """
        Ensure that a station can completed its operation
        """
        url = reverse('operation-completed', kwargs={"pk": self.operation.pk})
        response = self.client.post(
            url, HTTP_X_AUTHORIZATION=str(self.place.identifier))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_completed_operation_x_authorization_other(self):
        """
        Ensure that a station can't completed an operation of an other place
        """
        url = reverse('operation-completed', kwargs={"pk": self.operation2.pk})
        response = self.client.post(
            url, HTTP_X_AUTHORIZATION=str(self.place.identifier))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_completed_operation_superuser(self):
        """
        Ensure that a superuser can completed a operation
        """
        url = reverse('operation-completed', kwargs={"pk": self.operation.pk})
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_completed_operation_normal_user(self):
        """
        Ensure that a normal user can't completed a operation
        """
        url = reverse('operation-completed', kwargs={"pk": self.operation.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOperationsFilters(APITestCase):
    fixtures = ['actions']

    def setUp(self):
        self.user = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.place2 = PlaceFactory()
        self.pot1 = PotFactory(place=self.place)
        self.pot2 = PotFactory(place=self.place2)

        self.operation1_1 = OperationCompletedFactory(pot=self.pot1)
        self.operation1_2 = OperationFactory(pot=self.pot1)
        self.operation1_3 = OperationCompletedFactory(pot=self.pot1)
        self.operation1_4 = OperationFactory(pot=self.pot1)

        self.operation2_1 = OperationCompletedFactory(pot=self.pot2)
        self.operation2_2 = OperationFactory(pot=self.pot2)
        self.operation2_3 = OperationCompletedFactory(pot=self.pot2)
        self.operation2_4 = OperationFactory(pot=self.pot2)

    def test_operation_list_completed_filter(self):
        """
        Ensure that completed filter work
        """
        self.client.force_authenticate(user=self.user)

        url = "{0}?completed=0".format(reverse('operation-list'))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], self.operation1_4.id)
        self.assertEqual(result[1]['id'], self.operation1_2.id)

        url = "{0}?completed=1".format(reverse('operation-list'))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], self.operation1_3.id)
        self.assertEqual(result[1]['id'], self.operation1_1.id)

    def test_operation_list_ordering_filter(self):
        """
        Ensure that ordering filter work
        """
        self.client.force_authenticate(user=self.user)

        url = "{0}?ordering=-completed_at".format(reverse('operation-list'))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]['id'], self.operation1_4.id)
        self.assertEqual(result[1]['id'], self.operation1_2.id)
        self.assertEqual(result[2]['id'], self.operation1_3.id)
        self.assertEqual(result[3]['id'], self.operation1_1.id)

        url = "{0}?ordering=completed_at".format(reverse('operation-list'))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data.get('results', [])

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]['id'], self.operation1_3.id)
        self.assertEqual(result[1]['id'], self.operation1_1.id)
        self.assertEqual(result[2]['id'], self.operation1_4.id)
        self.assertEqual(result[3]['id'], self.operation1_2.id)
