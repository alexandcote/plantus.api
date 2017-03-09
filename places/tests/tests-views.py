from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authentication.factories import UserFactory
from places.factories import PlaceFactory
from places.models import Place


class TestsPlaceCreate(APITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_place_create_with_users(self):
        """
        Ensure that we could create a place with user
        """
        url = reverse('place-list')
        data = {
            'name': 'Villa #8',
            'users': [self.user.id],
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        place = Place.objects.get(name='Villa #8')
        self.assertEquals(place.name, data['name'])
        self.assertEqual(place.users.count(), 1)

    def test_place_create_with_no_users(self):
        """
        Ensure that we could create a place without a user
        """
        url = reverse('place-list')
        data = {'name': 'Villa #8'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        place = Place.objects.get(name='Villa #8')
        self.assertEquals(place.name, data['name'])
        self.assertEqual(place.users.count(), 1)
        self.assertEqual(place.users.first().id, self.user.id)

    def test_place_create_empty(self):
        """
        Ensure that we need parameters to create a place
        """
        url = reverse('place-list')
        data = {}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data)

        expected_error = {'name': ['This field is required.']}
        self.assertEqual(response.data, expected_error)


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
        result = response.data.get('results', [])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.place1.id)
        self.assertEqual(result[0]['name'], self.place1.name)

    def test_place_list_unauthenticated(self):
        """
        Ensure that not log users can't list places
        """
        url = reverse('place-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUpdatePlaces(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.place2 = PlaceFactory(users=(self.user2,))

    def test_update_place(self):
        """
       Ensure that we could update a place
       """
        url = reverse('place-detail', kwargs={"pk": self.place.pk})
        data = {
            'name': 'Villa #10',
            'users': [self.user.id],
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        place = Place.objects.get(name='Villa #10')
        self.assertEquals(place.name, data['name'])
        self.assertEqual(place.users.count(), 1)

        # Without name should raise a Bad Request
        data.pop('name')
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_place(self):
        """
        Ensure that a patch works
        """
        url = reverse('place-detail', kwargs={"pk": self.place.pk})
        data = {
            'name': 'Villa #10',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        place = Place.objects.get(name='Villa #10')
        self.assertEquals(place.name, data['name'])
        self.assertEqual(place.users.count(), 1)

    def test_update_other_place(self):
        """
       Ensure that you cannot update someone else place
       """
        url = reverse('place-detail', kwargs={"pk": self.place.pk})
        data = {
            'name': 'Villa #10',
            'users': [self.user2.id],
        }
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeletePlaces(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))

    def test_delete_place(self):
        """
        Ensure that a Delete should returns No Content
        """
        url = reverse('place-detail', kwargs={"pk": self.place.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_place(self):
        """
        Ensure you cannot delete other places
        """
        url = reverse('place-detail', kwargs={"pk": self.place.pk})
        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestRetrievePlaces(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))

    def test_retrieve_place(self):
        """
        Ensure you can retrieve a place
        """
        url = reverse('place-detail', kwargs={"pk": self.place.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = response.data
        self.assertEquals(result['name'], self.place.name)
        self.assertTrue(self.user.id in result['users'])

    def test_retrieve_other_place(self):
        """
        Ensure you cannot retrieve other places
        """
        url = reverse('place-detail', kwargs={"pk": self.place.pk})
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSearchPlace(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.place = PlaceFactory(users=(self.user,))
        self.place2 = PlaceFactory(users=(self.user2,))

    def test_place_search_by_user(self):
        """
        Ensure you can search a place by user
        """
        url = reverse('place-list')
        url += "?users={search}".format(search=self.user.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.place.id)
        self.assertEqual(result[0]['name'], self.place.name)

    def test_place_search_by_other_user(self):
        """
        Ensure you can't search a place from an other user
        """
        url = reverse('place-list')
        url += "?users={search}".format(search=self.user2.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        result = response.data.get('results', [])

        self.assertEqual(len(result), 0)
