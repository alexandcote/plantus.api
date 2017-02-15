from rest_framework.viewsets import ModelViewSet

from pots.models import Pot
from pots.permissions import PotsPermission
from pots.serializers import PotSerializer


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
