from rest_framework.response import Response
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

    def list(self, request, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        if not request.user.is_superuser:
            queryset = queryset.filter(place__users=request.user)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
