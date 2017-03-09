from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from pots.models import (
    Pot,
    TimeSerie
)
from pots.permissions import (
    PotsPermission,
    TimeSeriesPermission
)
from pots.serializers import (
    PotSerializer,
    TimeSeriesSerializer
)
from plantus.filters import DateFilter


class PotViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing pots.
    """
    queryset = Pot.objects.all().prefetch_related(
        Prefetch(
            'timeseries',
            queryset=TimeSerie.objects.order_by('-id'),
            to_attr="current_spec"
        )
    )
    permission_classes = [PotsPermission]
    serializer_class = PotSerializer
    filter_fields = ('place', 'place__users',)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if not user.is_superuser:
            queryset = queryset.filter(place__users=user)

        return queryset


class TimeSeriesViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing time series.
    """
    queryset = TimeSerie.objects.prefetch_related('pot', 'pot__place').all()
    permission_classes = [TimeSeriesPermission]
    serializer_class = TimeSeriesSerializer
    filter_fields = ('pot', 'pot__place',)
    filter_backends = (DjangoFilterBackend, DateFilter, OrderingFilter,)
    ordering_fields = ('date',)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if not user.is_superuser:
            queryset = queryset.filter(pot__place__users=user)

        return queryset
