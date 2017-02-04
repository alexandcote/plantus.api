from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class WelcomeView(APIView):
    """
    API endpoint for the welcome message.
    """
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, format=None):
        """
        Return the welcome message.
        """
        return Response({
            'users': reverse('user-list', request=request, format=format),
        })
