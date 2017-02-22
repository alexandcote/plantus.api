from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.decorators import detail_route
from rest_framework.viewsets import ModelViewSet

from pots.models import Pot, TimeSerie
from pots.permissions import PotsPermission, TimeSeriesPermission
from pots.serializers import PotSerializer, TimeSeriesSerializer
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


class TimeSeriesViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing time series.
    """
    queryset = TimeSerie.objects.prefetch_related('pot', 'pot__place').all()
    permission_classes = [TimeSeriesPermission]
    serializer_class = TimeSeriesSerializer
    filter_fields = ('pot', 'pot__place',)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if not user.is_superuser:
            queryset = queryset.filter(pot__place__users=user)

        return queryset