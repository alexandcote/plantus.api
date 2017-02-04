from rest_framework.viewsets import ModelViewSet

from places.models import Place
from places.serializers import (
    SimplePlaceSerializer,
    PlaceSerializer
)


class PlaceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class SimplePlaceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    model = Place
    queryset = Place.objects.all()
    serializer_class = SimplePlaceSerializer
