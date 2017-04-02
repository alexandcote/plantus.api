import uuid
import datetime
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from pots.models import (
    Pot,
    TimeSerie,
    Operation)
from pots.permissions import (
    PotsPermission,
    TimeSeriesPermission,
    OperationsPermission)
from pots.serializers import (
    PotsSerializer,
    TimeSeriesSerializer,
    OperationsSerializer
)
from plantus.filters import DateFilter, CompletedFilter


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
    serializer_class = PotsSerializer
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
    ordering = ('-date',)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if not user.is_superuser:
            queryset = queryset.filter(pot__place__users=user)

        return queryset


class OperationsViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing operations.
    """
    queryset = Operation.objects.prefetch_related('pot', 'pot__place').all()
    permission_classes = [OperationsPermission]
    serializer_class = OperationsSerializer
    filter_backends = (DjangoFilterBackend, CompletedFilter,)
    filter_fields = ('pot', 'pot__place',)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if user.is_anonymous:
            identifier = self.request.META.get('HTTP_X_AUTHORIZATION', '')

            try:
                identifier = uuid.UUID(identifier)
                queryset = queryset.filter(pot__place__identifier=identifier)
            except ValueError:
                pass
        elif user.is_authenticated and not user.is_superuser:
            queryset = queryset.filter(pot__place__users=user)

        return queryset

    @detail_route(methods=['post'])
    def completed(self, request, pk=None):
        operation = self.get_object()
        operation.completed_at = datetime.datetime.now()
        operation.save()

        return Response(status=HTTP_204_NO_CONTENT)
