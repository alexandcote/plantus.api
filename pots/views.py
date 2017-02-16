from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.decorators import detail_route
from rest_framework.viewsets import ModelViewSet

from pots.models import Pot
from pots.permissions import PotsPermission
from pots.serializers import PotSerializer
from pots.services import service_to_water_pot


class PotViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing pots.
    """
    queryset = Pot.objects.all()
    permission_classes = [PotsPermission]
    serializer_class = PotSerializer
    filter_fields = ('place', 'place__users',)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if not user.is_superuser:
            queryset = queryset.filter(place__users=user)

        return queryset

    @detail_route(methods=['post'])
    def water(self, request, pk=None):
        pot = self.get_object()
        service_to_water_pot(pot)
        return Response(status=HTTP_202_ACCEPTED)
