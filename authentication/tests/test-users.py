from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authentication.factories import UserFactory


class TestsNormalUsersRetrieve(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()

    def test_current_users_retrieve(self):
        """
        Ensure that the current user information are correct
        """
        url = reverse('user-detail', kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data
        place_url = reverse('user-places', kwargs={"pk": self.user.pk})
        self.assertEqual(result['id'], self.user.id)
        self.assertEqual(result['first_name'], self.user.first_name)
        self.assertEqual(result['last_name'], self.user.last_name)
        self.assertEqual(result['email'], self.user.email)
        self.assertTrue(result['url'].endswith(url))
        self.assertTrue(result['places'].endswith(place_url))

    def test_other_users_retrieve(self):
        """
        Ensure that the current user can't access to a other user
        """
        url = reverse('user-detail', kwargs={"pk": self.user2.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
