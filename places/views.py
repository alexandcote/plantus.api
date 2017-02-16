from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.viewsets import ModelViewSet

from places.models import Place
from places.permissions import PlacesPermission
from places.serializers import PlaceSerializer
from places.services import service_to_water_all_pots


class PlaceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing places.
    """
    queryset = Place.objects.prefetch_related('users', 'pots').all()
    permission_classes = [PlacesPermission]
    serializer_class = PlaceSerializer
    filter_fields = ('users',)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if not user.is_superuser:
            queryset = queryset.filter(users=user)

        return queryset

    @detail_route(methods=['post'])
    def water(self, request, pk=None):
        place = self.get_object()
        service_to_water_all_pots(place)
        return Response(status=HTTP_202_ACCEPTED)
