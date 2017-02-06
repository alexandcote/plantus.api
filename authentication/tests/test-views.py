from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authentication.factories import UserFactory
from authentication.models import User


class TestsUsersCreate(APITestCase):
    def test_users_create(self):
        """
        Ensure that we could create a user
        """
        url = reverse('user-list')
        data = {
            "first_name": "Wayne",
            "last_name": "Gretzky",
            "email": "wayne.gretzky@plantustest.com",
            "password": "qwer1234",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email="wayne.gretzky@plantustest.com")
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class TestsUsersList(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_users_list(self):
        """
        Ensure that normal user can't list all users
        """
        url = reverse('user-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestsUsersRetrieve(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()

    def test_current_users_retrieve(self):
        """
        Ensure that the current user information are correct with the
        /users/<id> endpoint
        """
        url = reverse('user-detail', kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data
        self.assertEqual(result['id'], self.user.id)
        self.assertEqual(result['first_name'], self.user.first_name)
        self.assertEqual(result['last_name'], self.user.last_name)
        self.assertEqual(result['email'], self.user.email)
        self.assertTrue(result['url'].endswith(url))
        self.assertEqual(len(result['places']), 0)

    def test_other_users_retrieve(self):
        """
        Ensure that the current user can't access to a other user with the
        /users/<id> endpoint
        """
        url = reverse('user-detail', kwargs={"pk": self.user2.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestsUsersUpdate(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()

    def test_users_partial_update(self):
        """
        Ensure that the user information are correctly updated
        """
        url = reverse('user-detail', kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.user)

        data = {"first_name": "Wayne", "last_name": "Gretzky"}
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, self.user.email)

    def test_other_users_partial_update(self):
        """
        Ensure that the user information are not updated
        """
        url = reverse('user-detail', kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.user2)

        data = {"first_name": "Wayne", "last_name": "Gretzky"}
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user = User.objects.get(pk=self.user.pk)
        self.assertNotEqual(user.first_name, data["first_name"])
        self.assertNotEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, self.user.email)

    def test_current_users_full_update(self):
        """
        Ensure that the user information are correctly updated with put
        """
        url = reverse('user-detail', kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.user)

        data = {
            "first_name": "Wayne",
            "last_name": "Gretzky",
            "email": "wayne.gretzky@sparetest.com",
            "password": "qwer1234"
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.check_password(data["password"]), True)

    def test_other_users_full_update(self):
        """
        Ensure that the other user information are not updated
        """
        url = reverse('user-detail', kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.user2)

        data = {
            "first_name": "Wayne",
            "last_name": "Gretzky",
            "email": "wayne.gretzky@sparetest.com",
            "password": "not_valide"
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user = User.objects.get(pk=self.user.pk)
        self.assertNotEqual(user.first_name, data["first_name"])
        self.assertNotEqual(user.last_name, data["last_name"])
        self.assertNotEqual(user.email, data["email"])
        self.assertEqual(user.email, self.user.email)
        self.assertEqual(user.check_password(data["password"]), False)


class TestsUsersDelete(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()

    def test_current_users_delete(self):
        """
        Ensure that user can't delete it self with the /users/<id> endpoint
        """
        url = reverse('user-detail', kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_users_delete(self):
        """
        Ensure that user can't delete other users with the /users/<id> endpoint
        """
        url = reverse('user-detail', kwargs={"pk": self.user2.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUsersCustomEndpoints(APITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_users_me(self):
        """
        Ensure that the current user information are correct with the
        /users/me endpoint
        """
        url = reverse('user-me')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data
        user_url = reverse('user-detail', kwargs={"pk": self.user.pk})
        self.assertEqual(result['id'], self.user.id)
        self.assertEqual(result['first_name'], self.user.first_name)
        self.assertEqual(result['last_name'], self.user.last_name)
        self.assertEqual(result['email'], self.user.email)
        self.assertTrue(result['url'].endswith(user_url))
        self.assertEqual(len(result['places']), 0)


class TestSuperUserList(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)

    def test_users_list(self):
        """
        Ensure that superuser can list all users
        """
        url = reverse('user-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSuperUsersDelete(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.user2 = UserFactory()

    def test_current_users_delete(self):
        """
        Ensure that user can't delete it self with the /users/<id> endpoint
        """
        url = reverse('user-detail', kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_other_users_delete(self):
        """
        Ensure that user can't delete other users with the /users/<id> endpoint
        """
        url = reverse('user-detail', kwargs={"pk": self.user2.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

# TODO: Add token test
