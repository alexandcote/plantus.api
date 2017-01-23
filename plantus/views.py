from rest_framework.response import Response
from rest_framework.views import APIView


class WelcomeView(APIView):
    """
    API endpoint for the welcome message.
    :param request:
    :return:
    """

    def get(self, request, format=None):
        """
        Return the welcome message.
        """
        return Response("Welcome to the PlantUS API")
