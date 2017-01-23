from unittest import TestCase
from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from plantus.dotenv_loader import load_dotenv_file


class TestsLoadEnv(TestCase):

    @mock.patch('plantus.dotenv_loader.join')
    @mock.patch('plantus.dotenv_loader.load_dotenv')
    def test_load_env(self, mock_env, mock_path):
        """
        Ensure the env loader calls the right function
        """
        path = 'my_path'
        mock_path.return_value = path
        load_dotenv_file()
        mock_env.assert_called_once_with(path)


class TestsWelcome(APITestCase):

    def test_welcome_view(self):
        """
        Ensure welcome route work
        """
        url = reverse('welcome')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
