from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.serializers import UserSerializer
from places.models import Place
from places.serializers import PlaceSerializer


class PlaceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @detail_route()
    def users(self, request, pk=None):
        place = self.get_object()
        serializer = UserSerializer(place.users.all(), context={
            'request': request}, many=True)
        return Response(serializer.data)
