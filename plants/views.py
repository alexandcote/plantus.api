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
