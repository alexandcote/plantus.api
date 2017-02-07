from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.serializers import UserSerializer
from places.models import Place
from places.permissions import PlacesPermission
from places.serializers import PlaceSerializer


class PlaceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Place.objects.filter()
    permission_classes = [PlacesPermission]
    serializer_class = PlaceSerializer

    def list(self, request, **kwargs):

        if request.user.is_superuser:
            queryset = Place.objects.all()
        else:
            queryset = Place.objects.filter(users=request.user)

        serializer = PlaceSerializer(
            queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @detail_route()
    def users(self, request, pk=None):
        place = self.get_object()
        serializer = UserSerializer(place.users.all(), context={
            'request': request}, many=True)
        return Response(serializer.data)
