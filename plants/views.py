from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from plants.models import Plant
from plants.permissions import PlantPermission
from plants.serializers import PlantSerializer


class PlantViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Plant.objects.filter()
    permission_classes = [PlantPermission]
    serializer_class = PlantSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'description',)
